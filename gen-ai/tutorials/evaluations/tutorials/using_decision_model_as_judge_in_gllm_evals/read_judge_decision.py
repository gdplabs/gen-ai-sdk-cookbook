import asyncio

from gllm_inference.dm_invoker import build_dm_invoker
from gllm_evals.metrics.generation.geval_completeness import GEvalCompletenessMetric
from gllm_evals.types import LLMTestCase


async def main():
    judge = build_dm_invoker(
        model_id="openrouter/typesafe/jev-1.13",
    )
    metric = GEvalCompletenessMetric(models=judge, threshold=1.0)
    case = LLMTestCase(
        input="When was Atlas founded, and who founded it?",
        actual_output="Atlas was founded in 1985.",
        expected_output="Atlas was founded in 1985 by Maria Lopez.",
    )

    result = await metric.evaluate(case)
    print(result.model_dump())


if __name__ == "__main__":
    asyncio.run(main())
