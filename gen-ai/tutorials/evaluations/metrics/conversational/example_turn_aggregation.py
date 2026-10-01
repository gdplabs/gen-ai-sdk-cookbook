"""Turn aggregation comparing MEAN, WORST_TURN and a custom aggregator on one conversation."""

import asyncio
import json

from dotenv import load_dotenv

from gllm_evals import ConversationalTestCase, Turn
from gllm_evals.aggregation import BaseTurnAggregator
from gllm_evals.constant import TurnAggregationMethod
from gllm_evals.metrics.generation.deepeval_faithfulness import DeepEvalFaithfulnessMetric

load_dotenv()

CONTRADICTED_SECOND_TURN = ConversationalTestCase(
    turns=[
        Turn(role="user", content="How much is a yoga session?"),
        Turn(
            role="assistant",
            content="Sessions are $25 each.",
            retrieved_context=["A single yoga session costs $25."],
        ),
        Turn(role="user", content="Did the price change this year?"),
        Turn(
            role="assistant",
            content="Still $25 per session.",
            retrieved_context=["As of January the price rose to $40 per session."],
        ),
        Turn(role="user", content="Do you offer packages?"),
        Turn(
            role="assistant",
            content="Yes, a 10-class pack is available.",
            retrieved_context=["We sell a 10-class pack."],
        ),
    ],
)


class FailIfTwoTurnsSlip(BaseTurnAggregator):
    """Fail the conversation as soon as two turns are unfaithful."""

    def aggregate(self, turn_scores: list[float]) -> float:
        """Return 0.0 when at least two turns scored below 1.0, else 1.0."""
        unfaithful = sum(1 for score in turn_scores if score < 1)
        return 0.0 if unfaithful >= 2 else 1.0


async def main():
    """Main function."""
    strategies = {
        "MEAN (default)": TurnAggregationMethod.MEAN,
        "WORST_TURN": TurnAggregationMethod.WORST_TURN,
        "FailIfTwoTurnsSlip (custom)": FailIfTwoTurnsSlip(),
    }

    for label, strategy in strategies.items():
        metric = DeepEvalFaithfulnessMetric(window_size=1, turn_aggregation=strategy)
        result = await metric.evaluate(CONTRADICTED_SECOND_TURN)
        payload = json.loads(result.model_dump_json())
        print(
            f"--- {label}: score={payload['score']} success={payload['success']} "
            f"turns_total={payload.get('turns_total')} "
            f"turns_unfaithful={payload.get('turns_unfaithful')}"
        )
        print(f"    {payload['explanation']}")

    try:
        DeepEvalFaithfulnessMetric(turn_aggregation="worst_turn")
    except TypeError as error:
        print(f"--- string form refused: {error}")


if __name__ == "__main__":
    asyncio.run(main())
