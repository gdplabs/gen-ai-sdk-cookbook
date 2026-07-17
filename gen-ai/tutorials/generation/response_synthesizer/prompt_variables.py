"""Response Synthesizer: Using Prompt Variables.

Demonstrates adding prompt variables to be injected into the prompt template.

Reference: https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/generation/response-synthesizer#using-prompt-variables
"""

import asyncio

from dotenv import load_dotenv

from gllm_generation.response_synthesizer import ResponseSynthesizer

load_dotenv()


async def main() -> None:
    synthesizer = ResponseSynthesizer.preset.stuff(
        model_id="openai/gpt-5-nano",
        system_template="Talk like a {role}.",
        user_template="Create a joke about {topic}.",
    )
    response = await synthesizer.synthesize(role="5 years old", topic="parrot")
    print(f"Response: {response}")


if __name__ == "__main__":
    asyncio.run(main())
