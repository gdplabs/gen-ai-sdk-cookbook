"""Step 0: Run a metric with no settings and see which judge it uses.

With no models set, the metric is judged by the SDK default, google/gemini-3.1-flash-lite.
This step needs GOOGLE_API_KEY.

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation/tutorials/switching_judge_model
"""

import asyncio

from dotenv import load_dotenv
from gllm_evals.metrics.generation.geval_completeness import GEvalCompletenessMetric

from test_cases import RETURNS_CASE

load_dotenv()


async def main():
    completeness = GEvalCompletenessMetric()
    result = await completeness.evaluate(RETURNS_CASE)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
