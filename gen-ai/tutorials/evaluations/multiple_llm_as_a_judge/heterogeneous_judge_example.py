"""Heterogeneous Multiple LLM-as-a-Judge Example

This tutorial demonstrates the Multiple LLM-as-a-Judge approach using
*different* models as judges. Each judge is a distinct model, and their
results are aggregated using ensemble methods.

Benefits:
1. Higher Alignment: Multiple judges provide more reliable evaluations
2. Faster Human Annotation: Humans only need to review cases with <100% agreement
3. Human Alignment: 100% agreement score indicates high alignment with human judgment
"""

import asyncio
import os

from gllm_evals.constant import AggregationMethod
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.types import LLMTestCase
from gllm_inference.lm_invoker import build_lm_invoker


async def main() -> None:
    """Run the heterogeneous multiple LLM-as-a-Judge example."""
    judges = [
        build_lm_invoker("openai/gpt-4o", os.getenv("OPENAI_API_KEY")),
        build_lm_invoker("openai/gpt-4o-mini", os.getenv("OPENAI_API_KEY")),
    ]
    evaluator = GEvalGenerationEvaluator(
        models=judges,
        aggregation_method=AggregationMethod.MAJORITY_VOTE,
    )

    data = LLMTestCase(
        input="What is the capital of France?",
        expected_output="Paris",
        actual_output="Paris",
        retrieved_context="Paris is the capital of France.",
    )
    result = await evaluator.evaluate(data)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
