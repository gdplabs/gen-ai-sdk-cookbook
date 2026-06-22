import asyncio
import json
from collections import defaultdict
from dotenv import load_dotenv
from gllm_core.retry import RetryConfig
from gllm_evals import EvalSuite, LLMTestCase, evaluate_suites
from gllm_evals.dataset.dict_dataset import DictDataset
from gllm_evals.evaluator.composite_evaluator import CompositeEvaluator
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.metrics.generation import (
    DeepEvalAnswerRelevancyMetric,
    GEvalCompletenessMetric,
    GEvalGroundednessMetric,
    GEvalRedundancyMetric,
)
from gllm_evals.metrics.retrieval import GEvalContextSufficiencyMetric
from gllm_evals.types import DefaultValues
from gllm_inference.lm_invoker import build_lm_invoker

from gllm_evals.aggregation import true_negative_rate, true_positive_rate

load_dotenv()

# ============================================================================
# Constants: Category → suite name mapping
# ============================================================================

CATEGORY_SUITE = {
    "default": "default",
    "default-multijudge": "default",
    "context_sufficiency": "context_sufficiency",
    "groundedness_2": "groundedness_2",
}


async def main() -> None:
    # ========================================================================
    # Load dataset from CSV
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

    grouped: dict[str, list] = defaultdict(list)
    for row, case in zip(rows, all_data):
        suite_name = CATEGORY_SUITE.get(row.get("category"))
        if suite_name:
            grouped[suite_name].append(case)

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
    # Run evaluations across all categories using evaluate_suites
    # ========================================================================

    result = await evaluate_suites(
        suites=[
            EvalSuite(name="default", data=grouped["default"], evaluators=[geval_evaluator]),
            EvalSuite(name="context_sufficiency", data=grouped["context_sufficiency"], evaluators=[composite_evaluator]),
            EvalSuite(name="groundedness_2", data=grouped["groundedness_2"], evaluators=[geval_groundedness_lenient]),
        ],
        dataset_name="calibration",
        run_aggregators=[true_negative_rate, true_positive_rate],
    )

    # ========================================================================
    # Output results and metrics
    # ========================================================================

    print(json.dumps(result.model_dump(), indent=2, default=repr))


if __name__ == "__main__":
    asyncio.run(main())
