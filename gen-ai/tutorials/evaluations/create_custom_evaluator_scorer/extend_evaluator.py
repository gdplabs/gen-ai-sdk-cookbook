"""
Custom Evaluator - Extending BaseEvaluator

This example demonstrates how to create a custom evaluator by extending
BaseEvaluator with your own evaluation logic.

Use this approach when:
- You need highly customized evaluation logic
- Built-in metrics don't fit your use case
- You have specific scoring requirements
"""

import asyncio

from gllm_evals.evaluator.evaluator import BaseEvaluator
from gllm_evals.metrics.metric import BaseMetric
from gllm_evals.types import EvaluatorResult, MetricInput, MetricOutput


class ExactMatchMetric(BaseMetric):
    """
    A custom metric that checks if the generated response exactly matches
    the expected response.
    """

    def __init__(self) -> None:
        super().__init__()
        self.name = "exact_match"

    async def _evaluate(self, data: MetricInput) -> MetricOutput:
        """Compare actual output with expected output."""
        score = int(data["actual_output"] == data["expected_output"])
        return {"score": score}


class ResponseEvaluator(BaseEvaluator):
    """
    A custom evaluator that uses the ExactMatchMetric.
    Demonstrates how to extend BaseEvaluator with your own logic.
    """

    def __init__(self) -> None:
        super().__init__(name="response_evaluator")
        self.metric = ExactMatchMetric()

    async def _evaluate(self, data: MetricInput) -> EvaluatorResult:
        """Evaluate the data using the custom metric."""
        return await self.metric.evaluate(data)


async def main() -> None:
    """Run the custom evaluator example."""
    from gllm_evals import LLMTestCase

    evaluator = ResponseEvaluator()
    data = LLMTestCase(
        input="What is the capital of France?",
        actual_output="Paris",
        expected_output="Paris",
    )
    result = await evaluator.evaluate(data)
    print("Custom Evaluator Result (Extending BaseEvaluator):")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
