"""Conversation completeness on a conversation that ignores two user intents and one that satisfies both."""

import asyncio
import json

from dotenv import load_dotenv

from gllm_evals import ConversationalTestCase, Turn
from gllm_evals.metrics.generation.deepeval_conversation_completeness import (
    DeepEvalConversationCompletenessMetric,
)

load_dotenv()

IGNORED = ConversationalTestCase(
    turns=[
        Turn(role="user", content="I need to change my flight and add a checked bag."),
        Turn(role="assistant", content="Anything else I can help with?"),
        Turn(role="user", content="And the bag?"),
        Turn(role="assistant", content="Anything else I can help with?"),
    ],
)

SATISFIED = ConversationalTestCase(
    turns=[
        Turn(role="user", content="I need to change my flight and add a checked bag."),
        Turn(
            role="assistant",
            content="I moved you to the 18:40 departure and added one checked bag.",
        ),
        Turn(role="user", content="And the bag fee?"),
        Turn(role="assistant", content="The checked bag fee is $35, charged to your card."),
    ],
)


async def main():
    """Main function."""
    metric = DeepEvalConversationCompletenessMetric()

    for label, conversation in (("ignored", IGNORED), ("satisfied", SATISFIED)):
        result = await metric.evaluate(conversation)
        print(f"--- {label}")
        print(json.dumps(json.loads(result.model_dump_json()), indent=2))


if __name__ == "__main__":
    asyncio.run(main())
