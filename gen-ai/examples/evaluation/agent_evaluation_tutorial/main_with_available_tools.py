"""Example of agent evaluation with available tools context.

This script demonstrates how to use the AgentEvaluator with the
DeepEvalToolCorrectnessMetric configured with available_tools parameter.

Providing available_tools context significantly improves evaluation accuracy by:
- Evaluating whether the agent selected the most appropriate tool from available options
- Checking if the agent missed better tool alternatives
- Providing context-aware reasoning about tool selection
"""

import asyncio
import os

from gllm_evals.constant import DefaultValues
from gllm_evals.dataset.simple_agent_tool_call_dataset import (
    load_simple_agent_tool_call_dataset,
    load_tool_schema,
)
from gllm_evals.evaluator.agent_evaluator import AgentEvaluator
from gllm_evals.metrics.agent.deepeval_tool_correctness import (
    DeepEvalToolCorrectnessMetric,
)


async def main() -> None:
    """Run agent evaluation with available tools context.

    Loads the tool schema and dataset, configures the tool correctness metric
    with available tools context, and evaluates the dataset item.
    """
    # Load tool schema - defines tools available to the agent
    available_tools = load_tool_schema("./dataset_examples")

    # Configure tool correctness metric with available tools
    # With available_tools, the evaluator can judge:
    # - Whether the agent selected the most appropriate tool
    # - If the agent missed better tool alternatives
    # - Context-aware reasoning about tool selection
    tool_correctness = DeepEvalToolCorrectnessMetric(
        model=DefaultValues.AGENT_EVALS_MODEL,
        model_credentials=os.getenv("OPENAI_API_KEY"),
        available_tools=available_tools,  # Provide tool context
    )

    # Create evaluator
    evaluator = AgentEvaluator(
        tool_correctness_metric=tool_correctness,
    )
    dataset = load_simple_agent_tool_call_dataset("./dataset_examples")
    result = await evaluator.evaluate(dataset[2])
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
