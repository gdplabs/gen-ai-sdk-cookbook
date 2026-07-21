"""Response Synthesizer: Customizing Extractor Function.

Demonstrates using a custom extractor function to get other attributes of the
LMOutput, or even the whole LMOutput object.

Reference: https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/generation/response-synthesizer#customizing-extractor-function
"""

import asyncio

from dotenv import load_dotenv

from gllm_generation.response_synthesizer import ResponseSynthesizer

load_dotenv()

query = "Name an animal that starts with the letter 'A'!"


def custom_extractor(response):
    return response


async def main() -> None:
    synthesizer = ResponseSynthesizer.preset.stuff(
        model_id="openai/gpt-5-nano",
        system_template="You are a helpful assistant.",
        user_template="{query}",
        config={"output_analytics": True},
        extractor_func=custom_extractor,
    )
    response = await synthesizer.synthesize(query=query)
    print(f"Response: {response}")


if __name__ == "__main__":
    asyncio.run(main())
