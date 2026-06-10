import asyncio
import json
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
    compute_combined_metrics,
    true_negative_rate,
    true_positive_rate,
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
    )


async def main() -> None:
    # ========================================================================
    # Load dataset from Google Sheets
    # ========================================================================

    dataset = DictDataset.from_csv(
        path="data/dataset.csv",
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
            retrieved_context=row["retrieved_context"],
            label=row["label"],
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
            run_aggregators=[true_negative_rate, true_positive_rate],
            experiment_tracker=_make_tracker("calibration-cat1"),
        ),
        evaluate(
            data=cat2_data,
            evaluators=[composite_evaluator],
            run_aggregators=[true_negative_rate, true_positive_rate],
            experiment_tracker=_make_tracker("calibration-cat2"),
        ),
        evaluate(
            data=cat3_data,
            evaluators=[geval_groundedness_lenient],
            run_aggregators=[true_negative_rate, true_positive_rate],
            experiment_tracker=_make_tracker("calibration-cat3"),
        ),
    )

    # ========================================================================
    # Output per-category results and metrics
    # ========================================================================

    def _dump(obj: object) -> str:
        return json.dumps(obj, indent=2, default=repr)

    print(_dump(results_cat1["results"]))
    print(_dump(results_cat1["run_aggregators_result"]))
    print(_dump(results_cat2["results"]))
    print(_dump(results_cat2["run_aggregators_result"]))
    print(_dump(results_cat3["results"]))
    print(_dump(results_cat3["run_aggregators_result"]))

    # ========================================================================
    # Aggregate metrics across all categories
    # ========================================================================

    combined = compute_combined_metrics(
        [
            (results_cat1, "generation", cat1_data),
            (results_cat2, "composite", cat2_data),
            (results_cat3, "generation", cat3_data),
        ]
    )
    print(_dump(combined))


if __name__ == "__main__":
    asyncio.run(main())
