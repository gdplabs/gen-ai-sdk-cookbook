"""Step 1: Use multiple judges on a metric.

Passes a list to `models`, so GPT, Gemini, and a model from OpenRouter all score the same test case.

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation/tutorials/switching_judge_model
"""

import asyncio
import json
import os

from dotenv import load_dotenv
from gllm_evals.metrics.generation.geval_completeness import GEvalCompletenessMetric
from gllm_inference.lm_invoker import build_lm_invoker

from test_cases import RETURNS_CASE

load_dotenv()


async def main():
    gpt = build_lm_invoker(model_id="openai/gpt-6-luna")
    gemini = build_lm_invoker(
        model_id="google/gemini-3.1-flash-lite",
        credentials=os.environ["GOOGLE_APPLICATION_CREDENTIALS"],
        config={
            "location": os.environ["GOOGLE_CLOUD_LOCATION"],
            "default_hyperparameters": {"labels": json.loads(os.environ["GOOGLE_VERTEX_LABEL"])},
        },
    )
    llama = build_lm_invoker(model_id="openrouter/meta-llama/llama-3.3-70b-instruct")

    multi_judge = GEvalCompletenessMetric(models=[gpt, gemini, llama])
    result = await multi_judge.evaluate(RETURNS_CASE)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
