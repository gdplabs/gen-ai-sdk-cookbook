import asyncio
import os

from gllm_evals import LLMTestCase
from gllm_evals.evaluator.composite_evaluator import CompositeEvaluator
from gllm_evals.metrics import (
    DeepEvalAnswerRelevancyMetric,
    GEvalCompletenessMetric,
    GEvalGroundednessMetric,
)
from gllm_inference.lm_invoker import build_lm_invoker


async def main() -> None:
    """Run the composite evaluator with built-in metrics example."""
    model = build_lm_invoker(
        model_id="openrouter/deepseek/deepseek-v4.1-flash-1017",
        credentials=os.getenv("OPENROUTER_API_KEY"),
        config={"provider": {"order": ["inference.net"], "allow_fallbacks": False}},
    )

    completeness = GEvalCompletenessMetric(models=model)
    groundedness = GEvalGroundednessMetric(models=model)
    relevancy = DeepEvalAnswerRelevancyMetric(models=model)

    evaluator = CompositeEvaluator(
        metrics=[completeness, groundedness, relevancy],
        name="generation_quality",
    )

    data = LLMTestCase(
        input="What is the capital of France?",
        actual_output="Paris is the capital city of France.",
        expected_output="Paris is the capital of France.",
        retrieved_context=["Paris is the capital city of France."],
    )
    result = await evaluator.evaluate(data)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
