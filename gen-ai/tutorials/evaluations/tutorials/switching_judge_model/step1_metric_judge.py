"""Step 1: Switch the judge on a metric.

Runs the completeness metric with a single GPT judge, a panel of GPT and Gemini, and GPT
with Gemini as the fallback judge.

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
    gpt = build_lm_invoker(model_id="openai/gpt-4o")
    gemini = build_lm_invoker(model_id="google/gemini-3.1-flash-lite")

    # One judge
    completeness = GEvalCompletenessMetric(models=gpt)
    result = await completeness.evaluate(RETURNS_CASE)
    print("=== One judge ===")
    print(result)

    # A panel of two judges from two providers
    panel = GEvalCompletenessMetric(models=[gpt, gemini])
    result = await panel.evaluate(RETURNS_CASE)
    print("\n=== Multiple judges ===")
    print(result)

    # GPT judges first; Gemini takes over only if GPT fails
    with_fallback = GEvalCompletenessMetric(models=gpt, fallback_models=[gemini])
    result = await with_fallback.evaluate(RETURNS_CASE)
    print("\n=== Fallback judge ===")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
