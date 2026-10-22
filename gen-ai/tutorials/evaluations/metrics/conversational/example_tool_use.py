"""Tool use on an agent that calls the wrong tool and one that calls the right one."""

import asyncio
import json

from dotenv import load_dotenv

from gllm_evals import ConversationalTestCase, ToolCall, Turn
from gllm_evals.metrics.tool_use.deepeval_tool_use import DeepEvalToolUseMetric

load_dotenv()

AVAILABLE_TOOLS = [
    {"name": "lookup_plan", "description": "Look up a plan's benefits and copays", "parameters": {"plan": "str"}},
    {"name": "get_weather", "description": "Get the weather forecast for a city", "parameters": {"city": "str"}},
]


def conversation(answer: str, tool_call: ToolCall) -> ConversationalTestCase:
    """Return the copay conversation answered after the given tool call."""
    return ConversationalTestCase(
        turns=[
            Turn(role="user", content="What is the physiotherapy copay on Plan Silver?"),
            Turn(role="assistant", content=answer, tools_called=[tool_call]),
        ],
    )


async def main():
    """Main function."""
    metric = DeepEvalToolUseMetric(available_tools=AVAILABLE_TOOLS)
    cases = (
        (
            "wrong_tool",
            conversation(
                "It is sunny in Paris today.",
                ToolCall(name="get_weather", input_parameters={"city": "Paris"}, output="sunny"),
            ),
        ),
        (
            "right_tool",
            conversation(
                "It is $60 per session.",
                ToolCall(name="lookup_plan", input_parameters={"plan": "silver"}, output="copay $60"),
            ),
        ),
    )

    for label, data in cases:
        result = await metric.evaluate(data)
        print(f"--- {label}")
        print(json.dumps(json.loads(result.model_dump_json()), indent=2))


if __name__ == "__main__":
    asyncio.run(main())
