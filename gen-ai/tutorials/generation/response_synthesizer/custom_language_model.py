"""Response Synthesizer: Customizing Language Model.

Demonstrates customizing language model config with custom prompt templates.

Reference: https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/generation/response-synthesizer#customizing-language-model
"""

import asyncio

from dotenv import load_dotenv

from gllm_generation.response_synthesizer import ResponseSynthesizer

load_dotenv()


async def main() -> None:
    synthesizer = ResponseSynthesizer.preset.stuff(
        model_id="openai/gpt-5-nano",
        system_template="Talk like a pirate.",
        user_template="Name an animal that starts with the letter 'A'!",
    )
    response = await synthesizer.synthesize()
    print(f"Response: {response}")


if __name__ == "__main__":
    asyncio.run(main())
