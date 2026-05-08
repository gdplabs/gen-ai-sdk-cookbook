"""Multiple LLM-as-a-Judge Example

This tutorial demonstrates the Multiple LLM-as-a-Judge approach, an advanced
evaluation method that uses multiple language models as judges to evaluate
tasks in parallel and aggregate their results using ensemble methods.

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
    """Run the homogeneous multiple LLM-as-a-Judge example.

    Uses the same model instantiated multiple times as judges.
    """
    model = build_lm_invoker(
        "google/gemini-3-flash-preview",
        os.getenv("GOOGLE_API_KEY"),
    )
    evaluator = GEvalGenerationEvaluator(
        models=[model] * 3,
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
