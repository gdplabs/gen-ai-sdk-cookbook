import asyncio
import os

from gllm_evals.dataset.simple_agent_tool_call_dataset import load_simple_agent_tool_call_dataset
from gllm_evals.evaluator.composite_evaluator import CompositeEvaluator
from gllm_evals.metrics.generation.geval_completeness import GEvalCompletenessMetric
from gllm_evals.metrics.generation.geval_groundedness import GEvalGroundednessMetric
from gllm_evals.metrics.generation.geval_redundancy import GEvalRedundancyMetric
from gllm_evals.metrics.tool_use.deepeval_tool_correctness import DeepEvalToolCorrectnessMetric
from gllm_inference.lm_invoker import build_lm_invoker


async def main() -> None:
    """Run basic agent evaluation on the first dataset item.

    Loads the agent tool call dataset, creates a CompositeEvaluator with the agent
    metrics, and evaluates the first item in the dataset.
    """
    dataset = load_simple_agent_tool_call_dataset('./dataset_examples').load()
    model = build_lm_invoker(
        model_id="openrouter/deepseek/deepseek-v4.1-flash-1017",
        credentials=os.getenv("OPENROUTER_API_KEY"),
        config={"provider": {"order": ["inference.net"], "allow_fallbacks": False}},
    )
    evaluator = CompositeEvaluator(
        name="agent",
        metrics=[
            DeepEvalToolCorrectnessMetric(models=model),
            GEvalCompletenessMetric(models=model),
            GEvalGroundednessMetric(models=model),
            GEvalRedundancyMetric(models=model),
        ],
    )
    result = await evaluator.evaluate(dataset[0])
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
