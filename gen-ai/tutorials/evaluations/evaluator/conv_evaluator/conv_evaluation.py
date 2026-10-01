"""ConvEvaluator: compose several conversational metrics over one conversation.

Scores a booking conversation that mostly succeeded and one that fell apart, so the aggregate
fields and the per-metric breakdown can be compared side by side.
"""

import asyncio
import json

from dotenv import load_dotenv

from gllm_evals import ConversationalTestCase, ToolCall, Turn
from gllm_evals.evaluator.conv_evaluator import ConvEvaluator
from gllm_evals.metrics.generation.deepeval_conversation_completeness import (
    DeepEvalConversationCompletenessMetric,
)
from gllm_evals.metrics.generation.deepeval_goal_accuracy import DeepEvalGoalAccuracyMetric
from gllm_evals.metrics.generation.deepeval_knowledge_retention import (
    DeepEvalKnowledgeRetentionMetric,
)

load_dotenv()

GOAL = "The assistant searches, presents options, and completes the booking."

SUCCESSFUL = ConversationalTestCase(
    turns=[
        Turn(role="user", content="Book me a flight to Paris next Friday."),
        Turn(
            role="assistant",
            content="I found two options: Air France $320 and Delta $410.",
            retrieved_context=["Air France CDG 09:15 $320", "Delta CDG 14:40 $410"],
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
            content="Booked Air France at $320. Your reference is AF-7821.",
            retrieved_context=["Booking AF-7821 confirmed: Air France, $320"],
        ),
        Turn(role="user", content="Remind me which airline and price?"),
        Turn(
            role="assistant",
            content="Air France, $320, reference AF-7821.",
            retrieved_context=["Booking AF-7821: Air France, $320"],
        ),
    ],
    chatbot_role="a helpful travel booking assistant",
    expected_output=GOAL,
)

FAILED = ConversationalTestCase(
    turns=[
        Turn(role="user", content="Book me a flight to Paris next Friday."),
        Turn(
            role="assistant",
            content="I found two options: Air France $320 and Delta $410.",
            retrieved_context=["Air France CDG 09:15 $320", "Delta CDG 14:40 $410"],
        ),
        Turn(role="user", content="Book the cheaper one."),
        Turn(
            role="assistant",
            content="Delta at $410 is the cheapest. I cannot book it for you.",
            retrieved_context=["Air France CDG 09:15 $320", "Delta CDG 14:40 $410"],
        ),
        Turn(role="user", content="Remind me which airline and price?"),
        Turn(
            role="assistant",
            content="You asked about a train to Berlin, I think. No price on file.",
            retrieved_context=["Booking: none. User asked about flights to Paris."],
        ),
    ],
    chatbot_role="a helpful travel booking assistant",
    expected_output=GOAL,
)


def build_evaluator() -> ConvEvaluator:
    """Build the evaluator used for both conversations.

    Returns:
        ConvEvaluator: Three conversation-level metrics, run concurrently.
    """
    return ConvEvaluator(
        metrics=[
            DeepEvalGoalAccuracyMetric(),
            DeepEvalKnowledgeRetentionMetric(),
            DeepEvalConversationCompletenessMetric(),
        ]
    )


async def main():
    """Score both conversations and print the full evaluator output for each."""
    for label, conversation in (("successful", SUCCESSFUL), ("failed", FAILED)):
        result = await build_evaluator().evaluate(conversation)
        print(f"\n{'=' * 70}\n{label}\n{'=' * 70}")
        for evaluator_name, output in result.items():
            print(json.dumps(json.loads(output.model_dump_json()), indent=2))


if __name__ == "__main__":
    asyncio.run(main())
