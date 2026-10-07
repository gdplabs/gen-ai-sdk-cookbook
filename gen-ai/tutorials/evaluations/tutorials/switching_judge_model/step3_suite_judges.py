"""Step 3: Switch the judge per suite with evaluate_suites().

The returns suite uses GPT for every metric. The shipping suite uses Gemini on groundedness
and GPT on everything else.

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
    gpt = build_lm_invoker(model_id="openai/gpt-4o")
    gemini = build_lm_invoker(model_id="google/gemini-3.1-flash-lite")

    result = await evaluate_suites(
        suites=[
            # Returns: GPT for every metric
            EvalSuite(
                name="returns",
                data=[RETURNS_CASE],
                evaluators=[GEvalGenerationEvaluator(models=gpt)],
            ),
            # Shipping: Gemini on groundedness, GPT on everything else
            EvalSuite(
                name="shipping",
                data=[SHIPPING_FEE_CASE, SHIPPING_DESTINATION_CASE],
                evaluators=[
                    GEvalGenerationEvaluator(
                        metrics=[
                            GEvalCompletenessMetric(models=gpt),
                            GEvalGroundednessMetric(models=gemini),
                            GEvalRedundancyMetric(models=gpt),
                        ],
                        refusal_metric=GEvalRefusalMetric(models=gpt),
                    )
                ],
            ),
        ],
    )
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
