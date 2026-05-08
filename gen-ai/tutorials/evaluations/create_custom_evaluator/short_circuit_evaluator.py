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
import logging

from gllm_evals.evaluator.evaluator import BaseEvaluator
from gllm_evals.types import MetricInput, EvaluatorResult


class ShortCircuitEvaluator(BaseEvaluator):
    """Evaluator that stops on first metric failure.

    Use case: completeness is the gate. If the output is incomplete,
    groundedness and redundancy checks are irrelevant — skip them.
    """

    def __init__(self, metrics, name="short_circuit_evaluator"):
        super().__init__(name=name, metrics=metrics)

    async def _evaluate(self, data: MetricInput) -> EvaluatorResult:
        combined_results = {}
        for metric in self.metrics:
            if not metric.can_evaluate(data):
                continue
            result = await metric.evaluate(data)
            combined_results[metric.name] = result

            if not result.success:
                # Stop here — remaining metrics skipped
                return combined_results

        return combined_results


# Usage
async def main():
    from gllm_evals import LLMTestCase
    from gllm_evals.metrics import (
        GEvalCompletenessMetric,
        GEvalGroundednessMetric,
        GEvalRedundancyMetric,
    )

    evaluator = ShortCircuitEvaluator(
        metrics=[
            GEvalCompletenessMetric(),
            GEvalGroundednessMetric(),
            GEvalRedundancyMetric(),
        ],
        name="fail_fast_generation",
    )

    data = LLMTestCase(
        input="What is the capital of France?",
        actual_output="New York",
        expected_output="Paris",
        retrieved_context="Paris is the capital of France.",
    )
    result = await evaluator.evaluate(data)
    # If completeness fails, groundedness and redundancy never run
    print(result)

if __name__ == "__main__":
    asyncio.run(main())