"""Step 1: Add a fallback judge to a metric.

GPT judges first. If its call fails, Gemini takes over.

To reproduce a failure, set OPENAI_API_KEY in .env to an invalid value such as "sk-invalid".
Don't delete the key instead: without it, build_lm_invoker() fails before any model is called,
so the fallback never starts.

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

    with_fallback = GEvalCompletenessMetric(models=gpt, fallback_models=[gemini])
    result = await with_fallback.evaluate(RETURNS_CASE)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
