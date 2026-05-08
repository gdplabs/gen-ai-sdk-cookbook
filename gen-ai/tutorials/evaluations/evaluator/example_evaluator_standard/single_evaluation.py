"""Evaluator Tutorial - Single Evaluation Example.

This tutorial demonstrates how to perform a single evaluation
using GEvalGenerationEvaluator with an LLMTestCase.
"""

import asyncio
import os

from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.types import LLMTestCase
from gllm_inference.lm_invoker import build_lm_invoker


async def main() -> None:
    """Run a single evaluation example."""
    data = LLMTestCase(
        input="What is the capital of France?",
        expected_output="Paris",
        actual_output="New York",
        retrieved_context="Paris is the capital of France.",
    )

    invoker = build_lm_invoker(
        model_id="google/gemini-3-flash-preview",
        credentials=os.getenv("GOOGLE_API_KEY"),
    )

    evaluator = GEvalGenerationEvaluator(model=invoker)
    result = await evaluator.evaluate(data)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
