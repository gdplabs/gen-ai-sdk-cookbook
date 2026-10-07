"""Turn relevancy on a conversation whose second reply goes off topic and one that stays on it."""

import asyncio
import json

from dotenv import load_dotenv

from gllm_evals import ConversationalTestCase, Turn
from gllm_evals.metrics.generation.deepeval_turn_relevancy import DeepEvalTurnRelevancyMetric

load_dotenv()

OFF_TOPIC = ConversationalTestCase(
    turns=[
        Turn(role="user", content="What is the carry-on baggage allowance?"),
        Turn(role="assistant", content="One cabin bag up to 7 kg is included on all fares."),
        Turn(role="user", content="Can I bring a second bag?"),
        Turn(role="assistant", content="Our lounges serve breakfast from 6 am."),
    ],
)

ON_TOPIC = ConversationalTestCase(
    turns=[
        Turn(role="user", content="What is the carry-on baggage allowance?"),
        Turn(role="assistant", content="One cabin bag up to 7 kg is included on all fares."),
        Turn(role="user", content="Can I bring a second bag?"),
        Turn(role="assistant", content="Yes, a second cabin bag can be added for $15."),
    ],
)


async def main():
    """Main function."""
    metric = DeepEvalTurnRelevancyMetric()

    for label, conversation in (("off_topic", OFF_TOPIC), ("on_topic", ON_TOPIC)):
        result = await metric.evaluate(conversation)
        print(f"--- {label}")
        print(json.dumps(json.loads(result.model_dump_json()), indent=2))


if __name__ == "__main__":
    asyncio.run(main())
