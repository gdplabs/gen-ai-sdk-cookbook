"""Turn contextual relevancy on a turn with relevant retrieval and one with unrelated retrieval."""

import asyncio
import json

from dotenv import load_dotenv

from gllm_evals import ConversationalTestCase, Turn
from gllm_evals.metrics.retrieval.deepeval_turn_contextual_relevancy import (
    DeepEvalTurnContextualRelevancyMetric,
)

load_dotenv()


def conversation(retrieved_context: list[str]) -> ConversationalTestCase:
    """Return the copay conversation with the given retrieved context."""
    return ConversationalTestCase(
        turns=[
            Turn(role="user", content="What is the physiotherapy copay on Plan Silver?"),
            Turn(
                role="assistant",
                content="The physiotherapy copay on Plan Silver is $60 per session.",
                retrieved_context=retrieved_context,
            ),
        ],
    )


async def main():
    """Main function."""
    metric = DeepEvalTurnContextualRelevancyMetric()
    cases = (
        ("relevant", ["Plan Silver: physiotherapy copay is $60 per session."]),
        ("unrelated", ["The Eiffel Tower is 330 metres tall.", "Bananas are rich in potassium."]),
    )

    for label, retrieved_context in cases:
        result = await metric.evaluate(conversation(retrieved_context))
        print(f"--- {label}")
        print(json.dumps(json.loads(result.model_dump_json()), indent=2))


if __name__ == "__main__":
    asyncio.run(main())
