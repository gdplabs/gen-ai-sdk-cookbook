"""Example of agent evaluation with trajectory accuracy metric.

This script demonstrates how to use the AgentEvaluator with the optional
LangChainAgentTrajectoryAccuracyMetric enabled. The trajectory accuracy metric
evaluates the agent's trajectory using LangChain's agentevals approach.

Note: The trajectory accuracy metric is disabled by default and only runs when
agent_trajectory and expected_agent_trajectory fields are present in the input data.
"""

import asyncio
import os

from gllm_evals.constant import DefaultValues
from gllm_evals.dataset.simple_agent_tool_call_dataset import load_simple_agent_tool_call_dataset
from gllm_evals.evaluator.agent_evaluator import AgentEvaluator
from gllm_evals.metrics.agent.langchain_agent_trajectory_accuracy import LangChainAgentTrajectoryAccuracyMetric

# Configure the trajectory accuracy metric (optional)
# This metric will only run when agent_trajectory is present in the input data
trajectory_accuracy = LangChainAgentTrajectoryAccuracyMetric(
    model=DefaultValues.AGENT_EVALS_MODEL,
    model_credentials=os.getenv("OPENAI_API_KEY"),
)

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
