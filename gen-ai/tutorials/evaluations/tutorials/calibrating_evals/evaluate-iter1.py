import asyncio
import json
import os
from dotenv import load_dotenv
from gllm_core.retry import RetryConfig
from gllm_evals import LLMTestCase
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
from gllm_evals.metrics.retrieval import GEvalContextSufficiencyMetric
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

CAT1_CATEGORIES = {"default", "default-multijudge"}
CAT2_CATEGORIES = {"context_sufficiency"}
CAT3_CATEGORIES = {"groundedness_2"}


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

    cat1_data, cat2_data, cat3_data = [], [], []
    for row, case in zip(rows, all_data):
        cat = row.get("category")
        if cat in CAT1_CATEGORIES:
            cat1_data.append(case)
        elif cat in CAT2_CATEGORIES:
            cat2_data.append(case)
        elif cat in CAT3_CATEGORIES:
            cat3_data.append(case)

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

    geval_groundedness_lenient = GEvalGenerationEvaluator(
        models=model,
        metrics=[
            GEvalGroundednessMetric(threshold=0.5),
            GEvalRedundancyMetric(),
            GEvalCompletenessMetric(),
        ],
    )
    geval_groundedness_lenient.refusal_metric = None

    composite_evaluator = CompositeEvaluator(
        metrics=[
            GEvalGroundednessMetric(models=model, threshold=0.5),
            GEvalContextSufficiencyMetric(models=model),
            DeepEvalAnswerRelevancyMetric(models=model),
        ],
        name="composite",
    )

    # ========================================================================
    # Run evaluations in parallel for all categories
    # ========================================================================

    results_cat1, results_cat2, results_cat3 = await asyncio.gather(
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

    # ========================================================================
    # Aggregate metrics across all categories
    # ========================================================================

    combined = compute_combined_metrics(
        [
            (results_cat1, "generation"),
            (results_cat2, "composite"),
            (results_cat3, "generation"),
        ]
    )
    print(json.dumps(combined, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
