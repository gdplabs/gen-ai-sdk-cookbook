"""Example of basic agent evaluation using AgentEvaluator.

This script demonstrates basic agent evaluation using the AgentEvaluator class.
The evaluator uses default metrics (DeepEvalToolCorrectnessMetric and
GEvalGenerationEvaluator) to assess agent performance.
"""

import asyncio

from gllm_evals.dataset.simple_agent_tool_call_dataset import load_simple_agent_tool_call_dataset
from gllm_evals.evaluator.agent_evaluator import AgentEvaluator


async def main() -> None:
    """Run basic agent evaluation on the first dataset item.

    Loads the agent tool call dataset, creates an AgentEvaluator with default
    metrics, and evaluates the first item in the dataset.
    """
    dataset = load_simple_agent_tool_call_dataset('./dataset_examples')
    evaluator = AgentEvaluator()
    result = await evaluator.evaluate(dataset[0])
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
