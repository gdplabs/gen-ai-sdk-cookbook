"""The default judge: run a metric on MiMo, set explicitly.

MiMo, openrouter/xiaomi/mimo-v2.6-flash, is the SDK's default judge. It is built here with the same
provider pin the SDK uses, so the script always shows which model judges and where to change it.

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation/tutorials/switching_judge_model
"""

import asyncio

from dotenv import load_dotenv
from gllm_evals.metrics.generation.geval_completeness import GEvalCompletenessMetric
from gllm_inference.lm_invoker import build_lm_invoker

from test_cases import RETURNS_CASE

load_dotenv()


async def main():
    mimo = build_lm_invoker(  # the default judge
        model_id="openrouter/xiaomi/mimo-v2.6-flash",
        config={"provider": {"order": ["makora"], "allow_fallbacks": False}},
    )

    completeness = GEvalCompletenessMetric(models=mimo)
    result = await completeness.evaluate(RETURNS_CASE)
    print(result.model_dump())


if __name__ == "__main__":
    asyncio.run(main())
