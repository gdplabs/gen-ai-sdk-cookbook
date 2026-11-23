"""Response Synthesizer: Adding Extra Contents.

Demonstrates adding extra contents such as attachments as additional context.

Reference: https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/generation/response-synthesizer#adding-extra-contents
"""

import asyncio

from dotenv import load_dotenv

from gllm_inference.schema import Attachment
from gllm_generation.response_synthesizer import ResponseSynthesizer

load_dotenv()


async def main() -> None:
    attachment = Attachment.from_path("path/to/tiger.jpg")
    query = "What animal is this?"

    synthesizer = ResponseSynthesizer.preset.stuff(
        model_id="openai/gpt-5-nano",
        system_template="You are a helpful assistant.",
        user_template="{query}",
    )
    response = await synthesizer.synthesize(query=query, extra_contents=[attachment])
    print(f"Response: {response}")


if __name__ == "__main__":
    asyncio.run(main())
