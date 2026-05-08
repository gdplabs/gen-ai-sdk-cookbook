import asyncio

from gllm_evals import LLMTestCase
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator


async def main() -> None:
    """Run a single evaluation example."""
    data = LLMTestCase(
        input="What is the capital of France?",
        expected_output="Paris",
        actual_output="New York",
        retrieved_context="Paris is the capital of France.",
    )

    evaluator = GEvalGenerationEvaluator()
    result = await evaluator.evaluate(data)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
