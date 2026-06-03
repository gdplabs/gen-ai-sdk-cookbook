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
        model_id="google/gemini-3-flash-preview",
        credentials=os.getenv("GOOGLE_API_KEY"),
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
