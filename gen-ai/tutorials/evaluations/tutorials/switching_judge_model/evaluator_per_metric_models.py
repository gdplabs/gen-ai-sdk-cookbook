"""Give each metric of an evaluator its own judge.

Jev, a decision model, judges completeness, redundancy, and the refusal check, where the verdict is enough.
MiMo judges groundedness, where a failing score needs the explanation of which claim is wrong.
The refusal check is not in `metrics`, so it gets its own `refusal_metric`.

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation/tutorials/switching_judge_model
"""

import asyncio

from dotenv import load_dotenv
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.metrics.generation.geval_completeness import GEvalCompletenessMetric
from gllm_evals.metrics.generation.geval_groundedness import GEvalGroundednessMetric
from gllm_evals.metrics.generation.geval_redundancy import GEvalRedundancyMetric
from gllm_evals.metrics.generation.geval_refusal import GEvalRefusalMetric
from gllm_inference.dm_invoker import build_dm_invoker
from gllm_inference.lm_invoker import build_lm_invoker

from test_cases import SHIPPING_FEE_CASE

load_dotenv()


async def main():
    jev = build_dm_invoker(model_id="openrouter/typesafe/jev-1.13")
    mimo = build_lm_invoker(
        model_id="openrouter/xiaomi/mimo-v2.6-flash",
        config={"provider": {"order": ["makora"], "allow_fallbacks": False}},
    )

    evaluator = GEvalGenerationEvaluator(
        metrics=[
            GEvalCompletenessMetric(models=jev),  # the verdict is enough
            GEvalGroundednessMetric(models=mimo),  # a failure needs the reason
            GEvalRedundancyMetric(models=jev),
        ],
        refusal_metric=GEvalRefusalMetric(models=jev),  # the refusal check is not in `metrics`, so set its judge here
    )
    result = await evaluator.evaluate(SHIPPING_FEE_CASE)
    print({name: out.model_dump() for name, out in result.items()})


if __name__ == "__main__":
    asyncio.run(main())
