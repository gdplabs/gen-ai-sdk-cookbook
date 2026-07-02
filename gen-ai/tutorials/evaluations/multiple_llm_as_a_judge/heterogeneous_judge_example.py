import asyncio
import os

from gllm_evals.constant import AggregationMethod
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.types import LLMTestCase
from gllm_inference.lm_invoker import build_lm_invoker


async def main() -> None:
    """Run the heterogeneous multiple LLM-as-a-Judge example."""
    judges = [
        build_lm_invoker(model_id="google/gemini-3-flash-preview", credentials=os.getenv("GOOGLE_API_KEY")),
        build_lm_invoker(model_id="google/gemini-2.5-flash-lite", credentials=os.getenv("GOOGLE_API_KEY")),
    ]
    evaluator = GEvalGenerationEvaluator(
        models=judges,
        aggregation_method=AggregationMethod.MAJORITY_VOTE,
        max_concurrent_judges=1,
    )

    data = LLMTestCase(
        input="What is the capital of France?",
        expected_output="Paris",
        actual_output="Paris",
        retrieved_context="Paris is the capital of France.",
        is_refusal=False,
    )
    result = await evaluator.evaluate(data)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
