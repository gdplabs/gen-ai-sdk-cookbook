"""Example of using the evaluate helper function with AgentEvaluator.

This script demonstrates how to use the evaluate() helper function with
AgentEvaluator for batch evaluation. The evaluate helper provides:
- Batch evaluation over entire datasets
- Automatic result aggregation
- Flexible inference function for generating agent responses
- Support for multiple evaluators
"""

import asyncio
import json

from gllm_evals.dataset.simple_agent_tool_call_dataset import load_simple_agent_tool_call_dataset
from gllm_evals.evaluate import evaluate
from gllm_evals.evaluator.agent_evaluator import AgentEvaluator


async def main() -> None:
    """Run batch agent evaluation using the evaluate helper function.

    Loads the dataset, defines an inference function to format agent responses,
    and runs batch evaluation using the evaluate() helper with AgentEvaluator.
    """
    dataset = load_simple_agent_tool_call_dataset('./dataset_examples')

    async def generate_agent_response(row):  # noqa: S7503
        """Generate agent response data for evaluation.

        Args:
            row: A single dataset item containing query, response, and tool information.

        Returns:
            A dictionary formatted for evaluation with all required fields.
        """
        return {
            "query": row.get("query"),
            "generated_response": row.get("generated_response"),
            "expected_response": row.get("expected_response"),
            "agent_trajectory": row.get("agent_trajectory", []),
            "expected_agent_trajectory": row.get("expected_agent_trajectory", []),
            "tools_called": row.get("tools_called", []),
            "expected_tools": row.get("expected_tools", [])
        }

    results = await evaluate(
        data=dataset,
        inference_fn=generate_agent_response,
        evaluators=[AgentEvaluator()],
    )
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
