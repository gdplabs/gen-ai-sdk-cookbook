import asyncio
import json
import os

from gllm_evals import EvalSuite, evaluate_suites
from gllm_evals.dataset.simple_agent_tool_call_dataset import (
    load_simple_agent_tool_call_dataset,
)
from gllm_evals.evaluator.composite_evaluator import CompositeEvaluator
from gllm_evals.metrics.generation.geval_completeness import GEvalCompletenessMetric
from gllm_evals.metrics.generation.geval_groundedness import GEvalGroundednessMetric
from gllm_evals.metrics.generation.geval_redundancy import GEvalRedundancyMetric
from gllm_evals.metrics.tool_use.deepeval_tool_correctness import (
    DeepEvalToolCorrectnessMetric,
)
from gllm_inference.lm_invoker import build_lm_invoker


async def main() -> None:
    """Run batch agent evaluation using the evaluate helper function.

    Loads the dataset as LLMTestCase objects, and runs batch evaluation using
    the evaluate() helper with a CompositeEvaluator.
    """
    data = load_simple_agent_tool_call_dataset("./dataset_examples").load()
    model = build_lm_invoker(
        model_id="openrouter/xiaomi/mimo-v2.6-flash",
        credentials=os.getenv("OPENROUTER_API_KEY"),
        config={"provider": {"order": ["makora"], "allow_fallbacks": False}},
    )

    suite = EvalSuite(
        data=data,
        evaluators=[
            CompositeEvaluator(
                name="agent",
                metrics=[
                    DeepEvalToolCorrectnessMetric(models=model),
                    GEvalCompletenessMetric(models=model),
                    GEvalGroundednessMetric(models=model),
                    GEvalRedundancyMetric(models=model),
                ],
            )
        ],
    )
    results = await evaluate_suites(
        suites=[suite],
    )
    print(json.dumps(results.model_dump(), indent=2))


if __name__ == "__main__":
    asyncio.run(main())
