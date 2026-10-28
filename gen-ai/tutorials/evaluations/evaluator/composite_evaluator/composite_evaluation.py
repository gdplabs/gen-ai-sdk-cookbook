import asyncio
import os
from pathlib import Path

from gllm_evals.dataset import DictDataset
from gllm_evals.evaluator.composite_evaluator import CompositeEvaluator
from gllm_evals.metrics import (
    DeepEvalContextualPrecisionMetric,
    DeepEvalContextualRecallMetric,
)
from gllm_inference.lm_invoker import build_lm_invoker


async def main() -> None:
    """Run a composite evaluation example."""
    model = build_lm_invoker(
        model_id="openrouter/deepseek/deepseek-v4.1-flash-1017",
        credentials=os.getenv("OPENROUTER_API_KEY"),
        config={"provider": {"order": ["inference.net"], "allow_fallbacks": False}},
    )

    # Create metrics using existing implementations
    contextual_recall = DeepEvalContextualRecallMetric(models=model)
    contextual_precision = DeepEvalContextualPrecisionMetric(models=model)

    # Create composite evaluator
    evaluator = CompositeEvaluator(
        metrics=[contextual_recall, contextual_precision],
        name="deepeval_contextual_evaluator",
    )

    # Load test data as LLMTestCase rows
    # Also loads from CSV: DictDataset.from_csv(...)
    data_path = Path(__file__).resolve().parent / "dataset_examples" / "simple_rag_data.jsonl"
    data = DictDataset.from_jsonl(str(data_path)).load()

    # Evaluate
    result = await evaluator.evaluate(data[0])
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
