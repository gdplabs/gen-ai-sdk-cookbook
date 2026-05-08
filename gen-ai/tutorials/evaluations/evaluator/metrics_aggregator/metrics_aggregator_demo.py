"""MetricsAggregator Tutorial.

This tutorial demonstrates how to use MetricsAggregator
to aggregate results from multiple metrics.

The MetricsAggregator has two overridable hooks:
1. compute_success(named_results) -> bool  (AND-gate)
2. compute_score(named_results) -> float  (polarity-aware mean)

You can also pass custom aggregators to any evaluator via
the metrics_aggregator parameter.
"""

import asyncio
import json

from gllm_evals import LLMTestCase
from gllm_evals.aggregation.metrics_aggregator import MetricsAggregator
from gllm_evals.evaluator.composite_evaluator import CompositeEvaluator
from gllm_evals.metrics.retrieval.ragas_context_precision import (
    RagasContextPrecisionWithoutReference,
)
from gllm_evals.metrics.retrieval.ragas_context_recall import RagasContextRecall


async def main() -> None:
    """Run a metrics aggregator demo example."""
    data = LLMTestCase(
        input="What is the capital of France?",
        expected_output="Paris",
        actual_output="Paris is the capital of France.",
        retrieved_context="Paris is the capital of France.",
    )

    # Create metrics using existing implementations
    contextual_recall = RagasContextRecall()
    contextual_precision = RagasContextPrecisionWithoutReference()

    # Create composite evaluator with default metrics aggregator
    evaluator = CompositeEvaluator(
        metrics=[contextual_recall, contextual_precision],
        name="demo_evaluator",
    )

    result = await evaluator.evaluate(data)
    print(json.dumps(result, indent=2))

    # Demonstrate direct MetricsAggregator usage
    aggregator = MetricsAggregator()
    print("\nMetricsAggregator instance created for custom aggregation.")
    print("Override compute_success or compute_score for custom logic.")


if __name__ == "__main__":
    asyncio.run(main())
