"""Switch the judge on an evaluator.

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
    gpt = build_lm_invoker(model_id="openrouter/openai/gpt-6-luna")

    evaluator = GEvalGenerationEvaluator(models=gpt)
    result = await evaluator.evaluate(RETURNS_CASE)
    print({name: out.model_dump() for name, out in result.items()})


if __name__ == "__main__":
    asyncio.run(main())
