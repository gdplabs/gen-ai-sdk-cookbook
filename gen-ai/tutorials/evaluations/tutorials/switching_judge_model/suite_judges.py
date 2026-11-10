"""Switch the judge per suite with evaluate_suites().

The returns suite uses DeepSeek for every metric. The shipping suite uses DeepSeek and GPT together on
groundedness, because its answers contain fees and delivery days that must match the policy.

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation/tutorials/switching_judge_model
"""

import asyncio

from dotenv import load_dotenv
from gllm_evals import EvalSuite, evaluate_suites
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.metrics.generation.geval_completeness import GEvalCompletenessMetric
from gllm_evals.metrics.generation.geval_groundedness import GEvalGroundednessMetric
from gllm_evals.metrics.generation.geval_redundancy import GEvalRedundancyMetric
from gllm_evals.metrics.generation.geval_refusal import GEvalRefusalMetric
from gllm_inference.lm_invoker import build_lm_invoker

from test_cases import RETURNS_CASE, SHIPPING_DESTINATION_CASE, SHIPPING_FEE_CASE

load_dotenv()


async def main():
    deepseek = build_lm_invoker(
        model_id="openrouter/deepseek/deepseek-v4.1-flash-1017",
        config={"provider": {"order": ["inference-net"], "allow_fallbacks": False}},
    )
    gpt = build_lm_invoker(
        model_id="openrouter/openai/gpt-6-luna",
        config={"provider": {"order": ["openai"], "allow_fallbacks": False}},
    )

    result = await evaluate_suites(
        suites=[
            # Returns: DeepSeek for every metric
            EvalSuite(
                name="returns",
                data=[RETURNS_CASE],
                evaluators=[GEvalGenerationEvaluator(models=deepseek)],
            ),
            # Shipping: DeepSeek and GPT on groundedness, DeepSeek on everything else
            EvalSuite(
                name="shipping",
                data=[SHIPPING_FEE_CASE, SHIPPING_DESTINATION_CASE],
                evaluators=[
                    GEvalGenerationEvaluator(
                        metrics=[
                            GEvalCompletenessMetric(models=deepseek),
                            GEvalGroundednessMetric(models=[deepseek, gpt]),  # two judges
                            GEvalRedundancyMetric(models=deepseek),
                        ],
                        refusal_metric=GEvalRefusalMetric(models=deepseek),
                    )
                ],
            ),
        ],
    )
    print(result.model_dump())


if __name__ == "__main__":
    asyncio.run(main())
