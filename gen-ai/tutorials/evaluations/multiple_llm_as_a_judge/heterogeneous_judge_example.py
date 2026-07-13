import asyncio

from gllm_evals.constant import AggregationMethod, DefaultValues
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.types import LLMTestCase
from gllm_inference.lm_invoker import build_lm_invoker
from dotenv import load_dotenv

load_dotenv()


async def main() -> None:
    """Run the heterogeneous multiple LLM-as-a-Judge example."""
    judges = [
        build_lm_invoker(model_id=DefaultValues.MODEL),
        build_lm_invoker(model_id="google/gemini-2.5-flash"),
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
        is_refusal=False,
    )
    result = await evaluator.evaluate(data)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
