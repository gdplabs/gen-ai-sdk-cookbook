"""Knowledge retention on a conversation that forgets an order number and one that recalls it."""

import asyncio
import json

from dotenv import load_dotenv

from gllm_evals import ConversationalTestCase, Turn
from gllm_evals.metrics.generation.deepeval_knowledge_retention import (
    DeepEvalKnowledgeRetentionMetric,
)

load_dotenv()

FORGETFUL = ConversationalTestCase(
    turns=[
        Turn(role="user", content="My order number is A-1234."),
        Turn(role="assistant", content="Thanks, I have noted order A-1234."),
        Turn(role="user", content="When will it arrive?"),
        Turn(role="assistant", content="Could you give me your order number?"),
    ],
    chatbot_role="a customer support assistant",
)

ATTENTIVE = ConversationalTestCase(
    turns=[
        Turn(role="user", content="My order number is A-1234 and I placed it last Monday."),
        Turn(role="assistant", content="Thanks, I have noted order A-1234 placed last Monday."),
        Turn(role="user", content="Can you remind me which order we are discussing?"),
        Turn(role="assistant", content="We are discussing order A-1234, which you placed last Monday."),
    ],
    chatbot_role="a customer support assistant",
)


async def main():
    """Main function."""
    metric = DeepEvalKnowledgeRetentionMetric()

    for label, conversation in (("forgetful", FORGETFUL), ("attentive", ATTENTIVE)):
        result = await metric.evaluate(conversation)
        print(f"--- {label}")
        print(json.dumps(json.loads(result.model_dump_json()), indent=2))


if __name__ == "__main__":
    asyncio.run(main())
