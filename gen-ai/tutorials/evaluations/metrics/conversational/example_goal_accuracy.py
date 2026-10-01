"""Goal accuracy on a completed booking and an abandoned one, judged against expected_output."""

import asyncio
import json

from dotenv import load_dotenv

from gllm_evals import ConversationalTestCase, ToolCall, Turn
from gllm_evals.metrics.generation.deepeval_goal_accuracy import DeepEvalGoalAccuracyMetric

load_dotenv()

GOAL = "The assistant searches, presents options, and completes the booking."

COMPLETED = ConversationalTestCase(
    turns=[
        Turn(role="user", content="Book me a flight to Paris next Friday."),
        Turn(
            role="assistant",
            content="I found two options: Air France $320 and Delta $410.",
            tools_called=[
                ToolCall(
                    name="search_flights",
                    input_parameters={"destination": "Paris", "date": "next Friday"},
                    output="Air France $320; Delta $410",
                )
            ],
        ),
        Turn(role="user", content="Book the cheaper one."),
        Turn(role="assistant", content="Booked Air France at $320. Your reference is AF-7821."),
    ],
    expected_output=GOAL,
)

ABANDONED = ConversationalTestCase(
    turns=[
        Turn(role="user", content="Book me a flight to Paris next Friday."),
        Turn(role="assistant", content="There are several flights to Paris."),
        Turn(role="user", content="Book the cheaper one."),
        Turn(role="assistant", content="I cannot book flights for you."),
    ],
    expected_output=GOAL,
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
