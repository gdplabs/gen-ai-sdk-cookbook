"""Step 2: Give each metric of an evaluator its own model.

Completeness and redundancy use GPT, and groundedness uses the default Gemini model.
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
from gllm_inference.lm_invoker import build_lm_invoker

from test_cases import RETURNS_CASE

load_dotenv()


async def main():
    gpt = build_lm_invoker(model_id="openai/gpt-6-luna")

    evaluator = GEvalGenerationEvaluator(
        metrics=[
            GEvalCompletenessMetric(models=gpt),
            GEvalGroundednessMetric(),  # no models: uses the default model, google/gemini-3.1-flash-lite
            GEvalRedundancyMetric(models=gpt),
        ],
        refusal_metric=GEvalRefusalMetric(models=gpt),  # the refusal check is not in `metrics`, so set its model here
    )
    result = await evaluator.evaluate(RETURNS_CASE)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
