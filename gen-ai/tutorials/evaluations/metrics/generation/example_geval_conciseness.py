import asyncio

from dotenv import load_dotenv
from gllm_inference.dm_invoker import build_dm_invoker
from gllm_evals.metrics.generation.geval_conciseness import GEvalConcisenessMetric
from gllm_evals.types import LLMTestCase

load_dotenv()


async def main():
    metric = GEvalConcisenessMetric(models=build_dm_invoker("openrouter/typesafe/jev-1.13"))
    data = LLMTestCase(
        input="What is the capital of France?",
        actual_output="I believe the capital of France is Paris. Hope this helps!",
    )
    result = await metric.evaluate(data)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
