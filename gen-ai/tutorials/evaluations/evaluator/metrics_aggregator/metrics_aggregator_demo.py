import asyncio
import json
import os

from gllm_evals import LLMTestCase
from gllm_evals.aggregation.metrics_aggregator import MetricsAggregator
from gllm_evals.evaluator.composite_evaluator import CompositeEvaluator
from gllm_evals.metrics import (
    DeepEvalContextualPrecisionMetric,
    DeepEvalContextualRecallMetric,
)
from gllm_inference.lm_invoker import build_lm_invoker


async def main() -> None:
    """Run a metrics aggregator demo example."""
    model = build_lm_invoker(
        model_id="openrouter/deepseek/deepseek-v4.1-flash-1017",
        credentials=os.getenv("OPENROUTER_API_KEY"),
        config={"provider": {"order": ["inference.net"], "allow_fallbacks": False}},
    )

    data = LLMTestCase(
        input="What is the capital of France?",
        expected_output="Paris",
        actual_output="Paris is the capital of France.",
        retrieved_context="Paris is the capital of France.",
    )

    # Create metrics using existing implementations
    contextual_recall = DeepEvalContextualRecallMetric(models=model)
    contextual_precision = DeepEvalContextualPrecisionMetric(models=model)

    # Create composite evaluator with default metrics aggregator
    evaluator = CompositeEvaluator(
        metrics=[contextual_recall, contextual_precision],
        name="demo_evaluator",
    )

    result = await evaluator.evaluate(data)
    print(json.dumps({name: output.model_dump(mode="json") for name, output in result.items()}, indent=2))

    # Demonstrate direct MetricsAggregator usage
    aggregator = MetricsAggregator()
    print("\nMetricsAggregator instance created for custom aggregation.")
    print("Override compute_success or compute_score for custom logic.")


if __name__ == "__main__":
    asyncio.run(main())
