import asyncio
import json
import os
from deepeval.metrics.g_eval import Rubric
from dotenv import load_dotenv
from gllm_core.retry import RetryConfig
from gllm_evals.types import LLMTestCase
from gllm_evals.dataset.dict_dataset import DictDataset
from gllm_evals.evaluate import evaluate
from gllm_evals.evaluator.composite_evaluator import CompositeEvaluator
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.experiment_tracker import CSVExperimentTracker
from gllm_evals.metrics.generation import (
    DeepEvalAnswerRelevancyMetric,
    GEvalCompletenessMetric,
    GEvalGroundednessMetric,
    GEvalRedundancyMetric,
)
from gllm_evals.metrics.retrieval.geval_context_sufficiency import (
    GEvalContextSufficiencyMetric,
)
from gllm_evals.types import DefaultValues
from gllm_inference.lm_invoker import build_lm_invoker

from aggregators import (
    _make_true_negative_rate,
    _make_true_positive_rate,
    compute_combined_metrics,
)

load_dotenv()

# ============================================================================
# Constants: Category mappings for test case filtering
# ============================================================================

CAT1_CATEGORIES = {"default"}
CAT2_CATEGORIES = {"context_sufficiency"}
CAT3_CATEGORIES = {"groundedness_2"}
CAT4_CATEGORIES = {"default-multijudge"}

# ============================================================================
# Constants: Custom rubric and evaluation criteria for context sufficiency
# ============================================================================

CONTEXT_SUFFICIENCY_CRITERIA = """Context Sufficiency (1-3) - evaluate whether a chatbot can answer a user's query using the information provided as context and chat history, including reasonable calculations or inferences from that information. You are not concerned with factual correctness or accuracy, but only whether the context contains enough information to answer the query through direct statements, calculation, or logical inference."""
CONTEXT_SUFFICIENCY_EVALUATION_STEPS = [
    "Consider the user's query, context, and chat history.",
    "Determine if the query can be answered using the provided context through: (a) direct information, (b) calculation from provided data, or (c) reasonable inference from related information.",
    "If the chat history is not provided, consider only the context.",
    "Provide a brief explanation of why the context does or does not contain sufficient information, including what calculation or inference would be needed if applicable.",
]
CONTEXT_SUFFICIENCY_FEW_SHOT = """FEW-SHOT EXAMPLES:

Example 1:
    Query: Who invented the linux os?
    Context: Bjarne Stroustrup invented C++
    Reason: The context does not provide any relevant information about the Linux OS or its inventor.
    Score: 1.

Example 2:
    Query: What was the name of the spaceship used for the moon landing in 1969?
    Context: In 1969, Neil Armstrong became the first person to walk on the moon.
    Reason: The context provided does not include any information about the name of the spaceship used for the moon landing. The query specifically asks for the name of the spaceship, which is not present in the context.
    Score: 1.

Example 3:
    Query: How much does YC invest in startups?
    Context: YC is a seed stage accelerator program. It was founded in 2005 by Paul Graham, Jessica Livingston, Trevor Blackwell, and Robert Tappan Morris.
    Reason: The context does not include any information about the amount YC invests in startups.
    Score: 1.

Example 4:
    Query: What are the specific operational hours and ticket prices for the National Museum on weekends?
    Context: The National Museum is open every day of the week.
    On weekdays, the museum operates from 9:00 AM to 5:00 PM.
    Weekend hours are slightly shorter, but the museum remains open to the public.
    Standard admission is $15 for adults, but weekend prices may vary.
    Reason: The context includes information about operational hours and ticket prices for the National Museum, but it does not specify the exact hours and prices for weekends. The statement "may vary" indicates uncertainty rather than calculable information.
    Score: 2.

Example 5:
    Query: Kapan bola lampu pijar praktis ditemukan?
    Context: Thomas Alva Edison mengembangkan banyak peralatan penting di abad ke-19.
    Salah satu penemuannya yang terpenting adalah bola lampu pijar praktis pertama.
    Penemuan bola lampu pijar tersebut didemonstrasikan pada tahun 1879.
    Reason: The context includes information about the discovery of the practical incandescent light bulb by Thomas Alva Edison in the 19th century, it specify the exact year when the practical incandescent light bulb was discovered.
    Score: 3.

Example 6:
    Query: What is the average temperature in City X during summer?
    Context: City X recorded temperatures of 28°C, 32°C, 30°C, and 34°C in June, July, and August 2025.
    Reason: The context provides specific temperature data points during summer months. The average can be calculated directly from the provided data: (28+32+30+34)/4 = 31°C.
    Score: 3.

Example 7:
    Query: How much profit does Company Y make per unit?
    Context: Company Y sells Product Z for $100. Manufacturing costs are $60 per unit.
    Reason: The context provides selling price and cost, allowing direct profit calculation: $100 - $60 = $40 per unit.
    Score: 3.

Example 8:
    Query: What is the total charter price for Plane A considering operational costs?
    Context: Plane A operates in Region B. Per-seat pricing is $300/night with 10 seats available. Similar planes in the region charge $2,500-$3,500 for full charters.
    Reason: While explicit operational costs are not provided, the per-seat pricing inherently reflects operational costs (businesses price above costs). The context allows estimation of charter price through calculation (10 × $300 = $3,000) and market comparison, though it requires assuming full occupancy.
    Score: 2.
"""
CONTEXT_SUFFICIENCY_RUBRIC = [
    Rubric(
        score_range=(1, 1),
        expected_outcome="The context does not contain relevant information to answer the query, even through calculation or reasonable inference. The information is completely missing or unrelated.",
    ),
    Rubric(
        score_range=(2, 2),
        expected_outcome="The context contains related information that allows partial answering through calculation or inference, but requires assumptions about missing variables or has multiple valid interpretations. The answer would be approximate or conditional.",
    ),
    Rubric(
        score_range=(3, 3),
        expected_outcome="The context contains all necessary information to fully answer the query, either directly stated or through straightforward calculation from provided data. No external assumptions needed.",
    ),
]

# ============================================================================
# Helpers: Tracker factory
# ============================================================================


def _make_tracker(output_dir: str) -> CSVExperimentTracker:
    return CSVExperimentTracker(
        project_name="calibration",
        output_dir=output_dir,
        extra_score_keys=["aggregate_score", "aggregate_success", "aggregate"],
        companion_fields=["success", "explanation"],
        include_eval_result=True,
    )


async def main() -> None:
    # ========================================================================
    # Load dataset from Google Sheets
    # ========================================================================

    dataset = await DictDataset.from_gsheets(
        sheet_id="1CVWqNzX_tdnvkV0fQ3NPDuEE9HtTXk8k2XtgIg6Ml6M",
        worksheet_name="calibrate-dataset-simplified",
        client_email=os.getenv("GOOGLE_SHEETS_CLIENT_EMAIL"),
        private_key=os.getenv("GOOGLE_SHEETS_PRIVATE_KEY"),
    )

    # ========================================================================
    # Build test cases with labels and few-shot examples
    # ========================================================================

    rows = list(dataset.load())
    all_data = [
        LLMTestCase(
            input=row["input"],
            actual_output=row["actual_output"],
            expected_output=row["expected_output"],
            retrieved_context=row["retrieved_context1"] + row["retrieved_context2"],
            label=row["label"],
            fewshot_completeness=row.get("fewshot_completeness"),
            fewshot_groundedness=row.get("fewshot_groundedness"),
        )
        for row in rows
    ]

    # ========================================================================
    # Filter test cases by category
    # ========================================================================

    cat1_data, cat2_data, cat3_data, cat4_data = [], [], [], []
    for row, case in zip(rows, all_data):
        cat = row.get("category")
        if cat in CAT1_CATEGORIES:
            cat1_data.append(case)
        elif cat in CAT2_CATEGORIES:
            cat2_data.append(case)
        elif cat in CAT3_CATEGORIES:
            cat3_data.append(case)
        elif cat in CAT4_CATEGORIES:
            cat4_data.append(case)

    # ========================================================================
    # Configure LLM model with retry strategy
    # ========================================================================

    model = build_lm_invoker(
        model_id=DefaultValues.MODEL,
        config={
            "retry_config": RetryConfig(max_retries=3, timeout=100),
        },
    )

    # ========================================================================
    # Create evaluators for each category
    # ========================================================================

    geval_evaluator = GEvalGenerationEvaluator(models=model)
    geval_evaluator.refusal_metric = None

    context_sufficiency_metric = GEvalContextSufficiencyMetric(
        models=model,
        rubric=CONTEXT_SUFFICIENCY_RUBRIC,
        criteria=CONTEXT_SUFFICIENCY_CRITERIA,
        evaluation_steps=CONTEXT_SUFFICIENCY_EVALUATION_STEPS,
        additional_context=CONTEXT_SUFFICIENCY_FEW_SHOT,
    )

    composite_evaluator = CompositeEvaluator(
        metrics=[
            context_sufficiency_metric,
            DeepEvalAnswerRelevancyMetric(models=model),
            GEvalGroundednessMetric(models=model, threshold=0.5),
        ],
        name="composite",
    )

    geval_groundedness_lenient = GEvalGenerationEvaluator(
        models=model,
        metrics=[
            GEvalGroundednessMetric(models=model, threshold=0.5),
            GEvalRedundancyMetric(),
            GEvalCompletenessMetric(),
        ],
    )
    geval_groundedness_lenient.refusal_metric = None

    geval_multijudge = GEvalGenerationEvaluator(
        models=[model] * 3,
    )
    geval_multijudge.refusal_metric = None

    # ========================================================================
    # Run evaluations in parallel for all categories
    # ========================================================================

    results_cat1, results_cat2, results_cat3, results_cat4 = await asyncio.gather(
        evaluate(
            data=cat1_data,
            evaluators=[geval_evaluator],
            run_aggregators=[
                _make_true_negative_rate("generation"),
                _make_true_positive_rate("generation"),
            ],
            experiment_tracker=_make_tracker("calibration-cat1"),
        ),
        evaluate(
            data=cat2_data,
            evaluators=[composite_evaluator],
            run_aggregators=[
                _make_true_negative_rate("composite"),
                _make_true_positive_rate("composite"),
            ],
            experiment_tracker=_make_tracker("calibration-cat2"),
        ),
        evaluate(
            data=cat3_data,
            evaluators=[geval_groundedness_lenient],
            run_aggregators=[
                _make_true_negative_rate("generation"),
                _make_true_positive_rate("generation"),
            ],
            experiment_tracker=_make_tracker("calibration-cat3"),
        ),
        evaluate(
            data=cat4_data,
            evaluators=[geval_multijudge],
            run_aggregators=[
                _make_true_negative_rate("generation"),
                _make_true_positive_rate("generation"),
            ],
            experiment_tracker=_make_tracker("calibration-cat4"),
        ),
    )

    # ========================================================================
    # Output per-category results and metrics
    # ========================================================================

    print(json.dumps(results_cat1["results"], indent=2))
    print(json.dumps(results_cat1["run_aggregators_result"], indent=2))
    print(json.dumps(results_cat2["results"], indent=2))
    print(json.dumps(results_cat2["run_aggregators_result"], indent=2))
    print(json.dumps(results_cat3["results"], indent=2))
    print(json.dumps(results_cat3["run_aggregators_result"], indent=2))
    print(json.dumps(results_cat4["results"], indent=2))
    print(json.dumps(results_cat4["run_aggregators_result"], indent=2))

    # ========================================================================
    # Aggregate metrics across all categories
    # ========================================================================

    combined = compute_combined_metrics(
        [
            (results_cat1, "generation"),
            (results_cat2, "composite"),
            (results_cat3, "generation"),
            (results_cat4, "generation"),
        ]
    )
    print(json.dumps(combined, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
