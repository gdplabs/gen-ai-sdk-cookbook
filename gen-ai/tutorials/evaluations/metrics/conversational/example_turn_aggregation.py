"""Turn aggregation: stop one contradicted answer being averaged away.

DeepEval averages the per-turn scores, so the same stale answer scores higher simply because
the conversation went on longer:

    exchanges  per-turn scores        MEAN   WORST_TURN
            2  [0.0, 1.0]             0.50         0.00
            3  [0.0, 1.0, 1.0]        0.67         0.00
            4  [0.0, 1.0, 1.0, 1.0]   0.75         0.00

WORST_TURN reports the least faithful turn instead, which fails at any length. `window_size=1`
judges each assistant turn against only its own retrieved context.
"""

import asyncio
import json

from dotenv import load_dotenv

from gllm_evals import ConversationalTestCase, Turn
from gllm_evals.aggregation import BaseTurnAggregator
from gllm_evals.constant import TurnAggregationMethod
from gllm_evals.metrics.generation.deepeval_faithfulness import DeepEvalFaithfulnessMetric

load_dotenv()

# The second assistant turn contradicts its own context: the retrieved price is $40, not $25.
STALE_ANSWER = ConversationalTestCase(
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
    """A team's own rule: fail the conversation as soon as two turns are unfaithful."""

    def aggregate(self, turn_scores: list[float]) -> float:
        """Return 0.0 once two or more turns scored below 1.0.

        Args:
            turn_scores (list[float]): One score per scored turn, in conversation order.

        Returns:
            float: 0.0 when at least two turns slipped, else 1.0.
        """
        unfaithful = sum(1 for score in turn_scores if score < 1)
        return 0.0 if unfaithful >= 2 else 1.0


async def main():
    """Score the same conversation under each aggregation strategy."""
    strategies = {
        "MEAN (default)": TurnAggregationMethod.MEAN,
        "WORST_TURN": TurnAggregationMethod.WORST_TURN,
        "FailIfTwoTurnsSlip (custom)": FailIfTwoTurnsSlip(),
    }

    for label, strategy in strategies.items():
        metric = DeepEvalFaithfulnessMetric(window_size=1, turn_aggregation=strategy)
        result = await metric.evaluate(STALE_ANSWER)
        payload = json.loads(result.model_dump_json())
        print(
            f"--- {label}: score={payload['score']} success={payload['success']} "
            f"turns_total={payload.get('turns_total')} "
            f"turns_unfaithful={payload.get('turns_unfaithful')}"
        )
        print(f"    {payload['explanation']}")

    # A bare string is rejected: the enum is what gives completion and a type error at the call site.
    try:
        DeepEvalFaithfulnessMetric(turn_aggregation="worst_turn")
    except TypeError as error:
        print(f"--- string form refused: {error}")


if __name__ == "__main__":
    asyncio.run(main())
