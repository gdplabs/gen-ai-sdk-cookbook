"""Step 0: Run a metric with no settings and see which model it uses.

With no models set, the metric uses the SDK default, openrouter/deepseek/deepseek-v4.1-flash-1017.
This step needs OPENROUTER_API_KEY.

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation/tutorials/switching_judge_model
"""

import asyncio

from dotenv import load_dotenv
from gllm_evals.metrics.generation.geval_completeness import GEvalCompletenessMetric

from test_cases import RETURNS_CASE

load_dotenv()


async def main():
    completeness = GEvalCompletenessMetric()  # no models: uses the default judge, DeepSeek V4.1 Flash on OpenRouter
    result = await completeness.evaluate(RETURNS_CASE)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
