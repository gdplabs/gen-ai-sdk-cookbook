"""Step 2: Switch the judge on an evaluator.

Sets one judge for every metric of GEvalGenerationEvaluator, shows that the evaluator's
models overrides a metric's models, then gives each metric its own judge.

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
from gllm_inference.lm_invoker import build_lm_invoker

from test_cases import RETURNS_CASE

load_dotenv()


async def main():
    gpt = build_lm_invoker(model_id="openai/gpt-4o")
    gemini = build_lm_invoker(model_id="google/gemini-3.1-flash-lite")

    # One judge for every metric
    evaluator = GEvalGenerationEvaluator(models=gpt)
    result = await evaluator.evaluate(RETURNS_CASE)
    print("=== One judge for every metric ===")
    print(result)

    # The evaluator's models overrides groundedness's models, so Gemini is never called
    evaluator = GEvalGenerationEvaluator(
        models=gpt,
        metrics=[
            GEvalCompletenessMetric(),
            GEvalGroundednessMetric(models=gemini),
            GEvalRedundancyMetric(),
        ],
    )
    result = await evaluator.evaluate(RETURNS_CASE)
    print("\n=== The evaluator wins ===")
    print(result)

    # A different judge per metric: leave the evaluator's models unset,
    # and pass refusal_metric so the refusal check doesn't use the default judge
    evaluator = GEvalGenerationEvaluator(
        metrics=[
            GEvalCompletenessMetric(models=gpt),
            GEvalGroundednessMetric(models=gemini),
            GEvalRedundancyMetric(models=gpt),
        ],
        refusal_metric=GEvalRefusalMetric(models=gpt),
    )
    result = await evaluator.evaluate(RETURNS_CASE)
    print("\n=== A different judge per metric ===")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
