"""Role adherence on an assistant that turns rude mid-conversation and one that stays in role."""

import asyncio
import json

from dotenv import load_dotenv

from gllm_evals import ConversationalTestCase, Turn
from gllm_evals.metrics.generation.deepeval_role_adherence import DeepEvalRoleAdherenceMetric

load_dotenv()

OUT_OF_ROLE = ConversationalTestCase(
    turns=[
        Turn(role="user", content="What is the physiotherapy copay on Plan Silver?"),
        Turn(role="assistant", content="Happy to help: it is $60 per session."),
        Turn(role="user", content="And how many sessions do I get?"),
        Turn(role="assistant", content="Read the policy yourself, I am busy."),
    ],
    chatbot_role="a polite health insurance support agent",
)

IN_ROLE = ConversationalTestCase(
    turns=[
        Turn(role="user", content="What is the physiotherapy copay on Plan Silver?"),
        Turn(role="assistant", content="Happy to help: it is $60 per session."),
        Turn(role="user", content="And how many sessions do I get?"),
        Turn(role="assistant", content="You get up to 20 sessions a year. Anything else I can check for you?"),
    ],
    chatbot_role="a polite health insurance support agent",
)


async def main():
    """Main function."""
    # One slip in two assistant turns scores 0.5, which passes the default threshold of 0.5
    metric = DeepEvalRoleAdherenceMetric(threshold=1.0)

    for label, conversation in (("out_of_role", OUT_OF_ROLE), ("in_role", IN_ROLE)):
        result = await metric.evaluate(conversation)
        print(f"--- {label}")
        print(json.dumps(json.loads(result.model_dump_json()), indent=2))


if __name__ == "__main__":
    asyncio.run(main())
