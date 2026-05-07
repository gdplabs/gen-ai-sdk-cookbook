"""Custom Evaluator - Combining Built-in Metrics

This example demonstrates how to use CompositeEvaluator to combine
any set of built-in metrics for your evaluation needs.

Use this approach when:
- You can use existing metrics
- You want to mix and match built-in metrics
- You need a simple, quick solution
"""

import asyncio

from gllm_evals import LLMTestCase
from gllm_evals.evaluator.composite_evaluator import CompositeEvaluator
from gllm_evals.metrics import (
    DeepEvalAnswerRelevancyMetric,
    GEvalCompletenessMetric,
    GEvalGroundednessMetric,
)


async def main() -> None:
    """Run the composite evaluator with built-in metrics example."""
    completeness = GEvalCompletenessMetric()
    groundedness = GEvalGroundednessMetric()
    relevancy = DeepEvalAnswerRelevancyMetric()

    evaluator = CompositeEvaluator(
        metrics=[completeness, groundedness, relevancy],
        name="generation_quality",
    )

    data = LLMTestCase(
        input="What is the capital of France?",
        actual_output="Paris is the capital city of France.",
        expected_output="Paris is the capital of France.",
        retrieved_context=["Paris is the capital city of France."],
    )
    result = await evaluator.evaluate(data)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
