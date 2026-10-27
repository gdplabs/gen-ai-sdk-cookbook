import asyncio
import os

from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.types import LLMTestCase
from gllm_inference.lm_invoker import build_lm_invoker


async def main() -> None:
    """Run a batch evaluation example."""
    data = [
        LLMTestCase(
            input="What is the capital of France?",
            expected_output="Paris",
            actual_output="New York",
            retrieved_context="Paris is the capital of France.",
        ),
        LLMTestCase(
            input="What is the capital of Japan?",
            expected_output="Tokyo",
            actual_output="Tokyo",
            retrieved_context="Tokyo is the capital of Japan.",
        ),
        LLMTestCase(
            input="What is the capital of Germany?",
            expected_output="Berlin",
            actual_output="Munich",
            retrieved_context="Berlin is the capital of Germany.",
        ),
    ]

    invoker = build_lm_invoker(
        model_id="google/gemini-3-flash-preview",
        credentials=os.getenv("GOOGLE_API_KEY"),
    )

    evaluator = GEvalGenerationEvaluator(models=invoker)
    results = await evaluator.evaluate(data)
    for idx, result in enumerate(results):
        print(f"Result {idx + 1}:")
        print(result)
        print()


if __name__ == "__main__":
    asyncio.run(main())
