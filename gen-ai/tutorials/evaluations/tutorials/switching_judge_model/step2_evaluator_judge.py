"""Step 2: Switch the model on an evaluator.

Set `models` once on the evaluator, and every metric uses that judge.

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation/tutorials/switching_judge_model
"""

import asyncio

from dotenv import load_dotenv
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_inference.lm_invoker import build_lm_invoker

from test_cases import RETURNS_CASE

load_dotenv()


async def main():
    evaluator = GEvalGenerationEvaluator(
        models=build_lm_invoker(
            model_id="openrouter/openai/gpt-6-luna",
            config={"provider": {"order": ["openai"], "allow_fallbacks": False}},
        )
    )
    result = await evaluator.evaluate(RETURNS_CASE)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
