"""Topic adherence on an assistant that declines an off-topic question and one that answers it."""

import asyncio
import json

from dotenv import load_dotenv

from gllm_evals import ConversationalTestCase, Turn
from gllm_evals.metrics.generation.deepeval_topic_adherence import DeepEvalTopicAdherenceMetric

load_dotenv()

ON_TOPIC = ConversationalTestCase(
    turns=[
        Turn(role="user", content="What is the carry-on baggage allowance?"),
        Turn(role="assistant", content="One cabin bag up to 7 kg is included on all fares."),
        Turn(role="user", content="Who do you think will win the election?"),
        Turn(role="assistant", content="I can only help with travel questions, such as baggage."),
    ],
    chatbot_role="an airline support assistant",
)

OFF_TOPIC = ConversationalTestCase(
    turns=[
        Turn(role="user", content="What is the carry-on baggage allowance?"),
        Turn(role="assistant", content="One cabin bag up to 7 kg is included on all fares."),
        Turn(role="user", content="Who do you think will win the election?"),
        Turn(role="assistant", content="Probably the incumbent, given current polling trends."),
    ],
    chatbot_role="an airline support assistant",
)


async def main():
    """Main function."""
    # One slip in two assistant turns scores 0.5, which passes the default threshold of 0.5
    metric = DeepEvalTopicAdherenceMetric(relevant_topics=["baggage policy", "flight changes"], threshold=1.0)

    for label, conversation in (("declined", ON_TOPIC), ("answered", OFF_TOPIC)):
        result = await metric.evaluate(conversation)
        print(f"--- {label}")
        print(json.dumps(json.loads(result.model_dump_json()), indent=2))


if __name__ == "__main__":
    asyncio.run(main())
