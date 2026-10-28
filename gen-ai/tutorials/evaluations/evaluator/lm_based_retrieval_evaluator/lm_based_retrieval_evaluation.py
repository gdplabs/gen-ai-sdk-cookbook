import asyncio
import os

from gllm_evals.evaluator.lm_based_retrieval_evaluator import LMBasedRetrievalEvaluator
from gllm_evals.types import LLMTestCase
from gllm_inference.lm_invoker import build_lm_invoker


async def main() -> None:
    """Run an LM-based retrieval evaluation example."""
    data = LLMTestCase(
        input="What is the capital of France?",
        expected_output="Paris is the capital of France.",
        retrieved_context=[
            "Berlin is the capital of Germany.",
            "Paris is the capital city of France with a population of over 2 million people.",
            "London is the capital of the United Kingdom.",
        ],
    )

    evaluator = LMBasedRetrievalEvaluator(
        models=build_lm_invoker(
            model_id="openrouter/deepseek/deepseek-v4.1-flash-1017",
            credentials=os.getenv("OPENROUTER_API_KEY"),
            config={"provider": {"order": ["inference.net"], "allow_fallbacks": False}},
        )
    )
    result = await evaluator.evaluate(data)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
