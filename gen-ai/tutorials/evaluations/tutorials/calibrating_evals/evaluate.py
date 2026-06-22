import asyncio
import json

from dotenv import load_dotenv
from gllm_core.retry import RetryConfig
from gllm_evals import EvalSuite, LLMTestCase, evaluate_suites
from gllm_evals.constant import DefaultValues
from gllm_evals.dataset.dict_dataset import DictDataset
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.experiment_tracker import CSVExperimentTracker
from gllm_inference.lm_invoker import build_lm_invoker

from gllm_evals.aggregation import true_negative_rate, true_positive_rate

load_dotenv()


async def main() -> None:
    # ========================================================================
    # Load dataset from CSV
    # ========================================================================

    dataset = DictDataset.from_csv(
        path="data/dataset.csv",
    )
    rows = dataset.load()

    # ========================================================================
    # Build test cases with labels
    # ========================================================================

    data = [
        LLMTestCase(
            input=row["input"],
            actual_output=row["actual_output"],
            expected_output=row["expected_output"],
            retrieved_context=row["retrieved_context"],
            label=row["label"],
        )
        for row in rows
    ]

    # ========================================================================
    # Configure evaluator and experiment tracker
    # ========================================================================

    evaluator = GEvalGenerationEvaluator(
        models=build_lm_invoker(
            model_id=DefaultValues.MODEL,
            config={
                "retry_config": RetryConfig(max_retries=3, timeout=100),
            },
        )
    )
    evaluator.refusal_metric = None

    experiment_tracker = CSVExperimentTracker(
        project_name="calibration",
        output_dir="calibration",
    )

    # ========================================================================
    # Run evaluation with metrics aggregation
    # ========================================================================

    result = await evaluate_suites(
        suites=[
            EvalSuite(
                name="calibration",
                data=data,
                evaluators=[evaluator],
            ),
        ],
        dataset_name="calibration",
        run_aggregators=[true_negative_rate, true_positive_rate],
        experiment_tracker=experiment_tracker,
    )

    # ========================================================================
    # Output results and metrics
    # ========================================================================

    print(json.dumps(result.model_dump(), indent=2))


if __name__ == "__main__":
    asyncio.run(main())
