import asyncio

from dotenv import load_dotenv
from gllm_inference.dm_invoker import build_dm_invoker
from gllm_inference.lm_invoker import build_lm_invoker
from gllm_evals.metrics.generation.geval_completeness import GEvalCompletenessMetric
from gllm_evals.types import LLMTestCase

load_dotenv()

CONFIDENCE_THRESHOLD = 0.8  # Calibrate against SME labels.


async def main():
    # Invokers read OPENROUTER_API_KEY and OPENAI_API_KEY from the environment.
    decision_metric = GEvalCompletenessMetric(
        models=build_dm_invoker("openrouter/typesafe/jev-1.13"),
        threshold=1.0,
    )
    stronger_metric = GEvalCompletenessMetric(
        models=build_lm_invoker("openai/gpt-6-luna"),
        threshold=1.0,
    )
    case = LLMTestCase(
        input="When was Atlas founded, and who founded it?",
        actual_output="Atlas was founded in 1985.",
        expected_output="Atlas was founded in 1985 by Maria Lopez.",
    )

    result = await decision_metric.evaluate(case)
    confidence = result.decision.confidence if result.decision is not None else None
    escalated = confidence is None or confidence < CONFIDENCE_THRESHOLD
    if escalated:
        result = await stronger_metric.evaluate(case)

    print("Initial confidence:", confidence)
    print("Escalated:", escalated)
    print("Final score:", result.score)
    print("Final judge:", result.model_id)


if __name__ == "__main__":
    asyncio.run(main())
