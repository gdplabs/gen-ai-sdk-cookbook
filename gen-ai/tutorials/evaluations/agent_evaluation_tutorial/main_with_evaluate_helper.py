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
    and runs batch evaluation using the evaluate() helper with AgentEvaluator.
    """
    rows = load_simple_agent_tool_call_dataset("./dataset_examples").load()

    data = [
        LLMTestCase(
            input=row.input,
            actual_output=row.actual_output,
            expected_output=row.expected_output,
            agent_trajectory=getattr(row, "agent_trajectory", []) or [],
            expected_agent_trajectory=getattr(row, "expected_agent_trajectory", []) or [],
            tools_called=getattr(row, "tools_called", []) or [],
            expected_tools=getattr(row, "expected_tools", []) or [],
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
