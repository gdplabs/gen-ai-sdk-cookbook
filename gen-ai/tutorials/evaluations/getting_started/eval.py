import asyncio
import os

from gllm_evals import LLMTestCase
from gllm_evals.metrics import GEvalCompletenessMetric
from gllm_inference.lm_invoker import build_lm_invoker


async def main() -> None:
    """Run a simple evaluation example."""
    metric = GEvalCompletenessMetric(
        models=build_lm_invoker(
            model_id="openrouter/deepseek/deepseek-v4.1-flash-1017",
            credentials=os.getenv("OPENROUTER_API_KEY"),
            config={"provider": {"order": ["inference.net"], "allow_fallbacks": False}},
        )
    )
    data = LLMTestCase(
        input="What is the capital of France?",
        actual_output="New York",
        expected_output="Paris is the capital of France.",
    )
    result = await metric.evaluate(data)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
