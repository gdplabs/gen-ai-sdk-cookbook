import asyncio
import os

from gllm_evals.dataset.simple_agent_tool_call_dataset import load_simple_agent_tool_call_dataset
from gllm_evals.evaluator.composite_evaluator import CompositeEvaluator
from gllm_evals.metrics.generation.geval_completeness import GEvalCompletenessMetric
from gllm_evals.metrics.generation.geval_groundedness import GEvalGroundednessMetric
from gllm_evals.metrics.generation.geval_redundancy import GEvalRedundancyMetric
from gllm_evals.metrics.tool_use.deepeval_tool_correctness import DeepEvalToolCorrectnessMetric
from gllm_evals.metrics.tool_use.langchain_agent_trajectory_accuracy import LangChainAgentTrajectoryAccuracyMetric
from gllm_inference.lm_invoker import build_lm_invoker

# Configure the trajectory accuracy metric (optional)
# This metric will only run when agent_trajectory is present in the input data
model = build_lm_invoker(
    model_id="openrouter/deepseek/deepseek-v4.1-flash-1017",
    credentials=os.getenv("OPENROUTER_API_KEY"),
    config={"provider": {"order": ["inference.net"], "allow_fallbacks": False}},
)
trajectory_accuracy = LangChainAgentTrajectoryAccuracyMetric(models=model)

# Create evaluator with trajectory accuracy metric
evaluator = CompositeEvaluator(
    name="agent",
    metrics=[
        DeepEvalToolCorrectnessMetric(models=model),
        GEvalCompletenessMetric(models=model),
        GEvalGroundednessMetric(models=model),
        GEvalRedundancyMetric(models=model),
        trajectory_accuracy,
    ],
)


async def main() -> None:
    """Run agent evaluation with trajectory accuracy metric.

    Loads the agent tool call dataset and evaluates an item using the
    CompositeEvaluator configured with the trajectory accuracy metric.
    """
    dataset = load_simple_agent_tool_call_dataset('./dataset_examples').load()
    result = await evaluator.evaluate(dataset[1])
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
