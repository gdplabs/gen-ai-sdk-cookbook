"""Goal accuracy on a completed booking and an abandoned one."""

import asyncio
import json

from dotenv import load_dotenv

from gllm_evals import ConversationalTestCase, ToolCall, Turn
from gllm_evals.metrics.generation.deepeval_goal_accuracy import DeepEvalGoalAccuracyMetric

load_dotenv()

COMPLETED = ConversationalTestCase(
    turns=[
        Turn(role="user", content="Find me flights to Paris next Friday."),
        Turn(
            role="assistant",
            content=(
                "I'll search next Friday's flights to Paris and sort them by price. "
                "Found two: Air France $320 and Delta $410."
            ),
            tools_called=[
                ToolCall(
                    name="search_flights",
                    input_parameters={"destination": "Paris", "date": "next Friday"},
                    output="Air France $320; Delta $410",
                )
            ],
        ),
        Turn(role="user", content="Book the cheaper one."),
        Turn(
            role="assistant",
            content="I'll book the cheaper option, Air France at $320. Done: your reference is AF-7821.",
            tools_called=[
                ToolCall(name="book_flight", input_parameters={"flight": "Air France $320"}, output="AF-7821")
            ],
        ),
    ],
)

ABANDONED = ConversationalTestCase(
    turns=[
        Turn(role="user", content="Book me a flight to Paris next Friday."),
        Turn(role="assistant", content="There are several flights to Paris."),
        Turn(role="user", content="Book the cheaper one."),
        Turn(role="assistant", content="I cannot book flights for you."),
    ],
)


async def main():
    """Main function."""
    metric = DeepEvalGoalAccuracyMetric()

    for label, conversation in (("completed", COMPLETED), ("abandoned", ABANDONED)):
        result = await metric.evaluate(conversation)
        print(f"--- {label}")
        print(json.dumps(json.loads(result.model_dump_json()), indent=2))


if __name__ == "__main__":
    asyncio.run(main())
