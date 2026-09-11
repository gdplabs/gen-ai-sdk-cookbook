import asyncio
import json

from gllm_evals import EvalSuite, LLMTestCase, evaluate_suites
from gllm_evals.dataset.simple_agent_tool_call_dataset import (
    load_simple_agent_tool_call_dataset,
)
from gllm_evals.evaluator.agent_evaluator import AgentEvaluator


async def main() -> None:
    """Run batch agent evaluation using the evaluate helper function.

    Loads the dataset, formats agent responses into LLMTestCase objects,
    and runs batch evaluation using the evaluate_suites() helper with AgentEvaluator.
    """
    rows = load_simple_agent_tool_call_dataset("./dataset_examples")

    data = [
        LLMTestCase(
            input=row.get("query", row.get("input", "")),
            actual_output=row.get("generated_response", row.get("actual_output", "")),
            expected_output=row.get(
                "expected_response", row.get("expected_output", "")
            ),
            agent_trajectory=row.get("agent_trajectory", []),
            expected_agent_trajectory=row.get("expected_agent_trajectory", []),
            tools_called=row.get("tools_called", []),
            expected_tools=row.get("expected_tools", []),
        )
        for row in rows
    ]

    suite = EvalSuite(
        data=data,
        evaluators=[AgentEvaluator()],
    )
    results = await evaluate_suites(
        suites=[suite],
    )
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
