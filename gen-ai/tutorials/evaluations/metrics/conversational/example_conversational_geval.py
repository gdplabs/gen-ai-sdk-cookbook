"""Conversational GEval scoring one conversation against a custom criterion."""

import asyncio
import json

from dotenv import load_dotenv

from gllm_evals import ConversationalTestCase, Turn
from gllm_evals.metrics.generation.deepeval_conversational_geval import (
    DeepEvalConversationalGEvalMetric,
)

load_dotenv()

CONVERSATION = ConversationalTestCase(
    turns=[
        Turn(role="user", content="What are the side effects of ibuprofen?"),
        Turn(
            role="assistant",
            content="Common side effects include stomach upset, nausea, and headache.",
            retrieved_context=["Ibuprofen is an NSAID. Side effects include GI irritation."],
        ),
        Turn(role="user", content="Is it safe with my blood thinner?"),
        Turn(
            role="assistant",
            content="Combining them raises bleeding risk. Please confirm with your pharmacist.",
            retrieved_context=["NSAIDs with warfarin: increased bleeding risk."],
        ),
    ],
    chatbot_role="a cautious health information assistant",
    expected_output="The assistant answers accurately and defers clinical decisions to a professional.",
)


async def main():
    """Main function."""
    metric = DeepEvalConversationalGEvalMetric(
        name="conversation_helpfulness",
        criteria=(
            "Judge whether the assistant made real progress on the user's goal across the "
            "whole conversation, using the expected outcome as the reference for success."
        ),
        threshold=0.6,
    )
    result = await metric.evaluate(CONVERSATION)
    print(json.dumps(json.loads(result.model_dump_json()), indent=2))


if __name__ == "__main__":
    asyncio.run(main())
