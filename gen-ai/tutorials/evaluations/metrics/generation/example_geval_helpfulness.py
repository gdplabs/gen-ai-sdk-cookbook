import asyncio

from dotenv import load_dotenv
from gllm_inference.dm_invoker import build_dm_invoker
from gllm_evals.metrics.generation.geval_helpfulness import GEvalHelpfulnessMetric
from gllm_evals.types import LLMTestCase

load_dotenv()


async def main() -> None:
    """Evaluate response helpfulness with an OpenRouter judge."""
    metric = GEvalHelpfulnessMetric(models=build_dm_invoker("openrouter/typesafe/jev-1.13"))
    data = LLMTestCase(
        input="How do I reverse a list in Python?",
        actual_output=(
            "Use slicing: `my_list[::-1]` returns a reversed copy, "
            "or call `my_list.reverse()` to reverse it in place."
        ),
    )
    result = await metric.evaluate(data)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
