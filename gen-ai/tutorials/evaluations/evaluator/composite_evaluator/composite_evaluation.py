import asyncio
from pathlib import Path

from gllm_evals import LLMTestCase
from gllm_evals.dataset import load_simple_rag_dataset
from gllm_evals.evaluator.composite_evaluator import CompositeEvaluator
from gllm_evals.metrics import (
    DeepEvalContextualPrecisionMetric,
    DeepEvalContextualRecallMetric,
)


async def main() -> None:
    """Run a composite evaluation example."""
    # Create metrics using existing implementations
    contextual_recall = DeepEvalContextualRecallMetric()
    contextual_precision = DeepEvalContextualPrecisionMetric()

    # Create composite evaluator
    evaluator = CompositeEvaluator(
        metrics=[contextual_recall, contextual_precision],
        name="deepeval_contextual_evaluator",
    )

    # Load test data
    csv_dir = Path(__file__).resolve().parent.parent / "create_custom_evaluator" / "dataset_examples"
    raw = load_simple_rag_dataset(current_dir=csv_dir)
    data = [
        LLMTestCase(
            input=row.input,
            actual_output=row.actual_output,
            expected_output=row.expected_output,
            retrieved_context=row.retrieved_context,
        )
        for row in raw.load()
    ]

    # Evaluate
    result = await evaluator.evaluate(data[0])
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
