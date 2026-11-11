"""The default judge: run a metric on DeepSeek, set explicitly.

DeepSeek, openrouter/deepseek/deepseek-v4.1-flash-1017, is the SDK's default judge. It is built here with the same
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
    deepseek = build_lm_invoker(  # the default judge
        model_id="openrouter/deepseek/deepseek-v4.1-flash-1017",
        config={"provider": {"order": ["inference-net"], "allow_fallbacks": False}},
    )

    completeness = GEvalCompletenessMetric(models=deepseek)
    result = await completeness.evaluate(RETURNS_CASE)
    print(result.model_dump())


if __name__ == "__main__":
    asyncio.run(main())
