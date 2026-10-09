"""Turn contextual precision on a turn whose relevant document is ranked first and one where it is ranked last."""

import asyncio
import json

from dotenv import load_dotenv

from gllm_evals import ConversationalTestCase, Turn
from gllm_evals.metrics.retrieval.deepeval_turn_contextual_precision import (
    DeepEvalTurnContextualPrecisionMetric,
)

load_dotenv()

RELEVANT = "Plan Silver: physiotherapy copay is $60 per session."
NOISE = ["The Eiffel Tower is 330 metres tall.", "Bananas are rich in potassium."]
EXPECTED = "The assistant states the $60 physiotherapy copay."


def conversation(retrieved_context: list[str]) -> ConversationalTestCase:
    """Return the copay conversation with the given retrieval ranking."""
    return ConversationalTestCase(
        turns=[
            Turn(role="user", content="What is the physiotherapy copay on Plan Silver?"),
            Turn(
                role="assistant",
                content="The physiotherapy copay on Plan Silver is $60 per session.",
                retrieved_context=retrieved_context,
            ),
        ],
        expected_output=EXPECTED,
    )


async def main():
    """Main function."""
    metric = DeepEvalTurnContextualPrecisionMetric()

    for label, ranking in (("relevant_first", [RELEVANT, *NOISE]), ("relevant_last", [*NOISE, RELEVANT])):
        result = await metric.evaluate(conversation(ranking))
        print(f"--- {label}")
        print(json.dumps(json.loads(result.model_dump_json()), indent=2))


if __name__ == "__main__":
    asyncio.run(main())
