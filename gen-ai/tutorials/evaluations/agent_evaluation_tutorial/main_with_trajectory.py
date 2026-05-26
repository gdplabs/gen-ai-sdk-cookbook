import asyncio
import os

from gllm_evals.constant import DefaultValues
from gllm_evals.dataset.simple_agent_tool_call_dataset import load_simple_agent_tool_call_dataset
from gllm_evals.evaluator.agent_evaluator import AgentEvaluator
from gllm_evals.metrics.tool_use.langchain_agent_trajectory_accuracy import LangChainAgentTrajectoryAccuracyMetric
from gllm_inference.lm_invoker import build_lm_invoker

# Configure the trajectory accuracy metric (optional)
# This metric will only run when agent_trajectory is present in the input data
model = build_lm_invoker(model_id=DefaultValues.MODEL, credentials=os.getenv("GOOGLE_API_KEY"))
trajectory_accuracy = LangChainAgentTrajectoryAccuracyMetric(models=model)

# Create evaluator with trajectory accuracy metric
evaluator = AgentEvaluator(
    trajectory_accuracy_metric=trajectory_accuracy
)


async def main() -> None:
    """Run agent evaluation with trajectory accuracy metric.

    Loads the agent tool call dataset and evaluates an item using the
    AgentEvaluator configured with the trajectory accuracy metric.
    """
    dataset = load_simple_agent_tool_call_dataset('./dataset_examples')
    result = await evaluator.evaluate(dataset[1])
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
