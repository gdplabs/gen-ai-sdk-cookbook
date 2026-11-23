"""Response Synthesizer: Adding History.

Demonstrates adding history as additional context for the language model.

Reference: https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/generation/response-synthesizer#adding-history
"""

import asyncio

from dotenv import load_dotenv

from gllm_inference.schema import Message
from gllm_generation.response_synthesizer import ResponseSynthesizer

load_dotenv()


async def main() -> None:
    history = [
        Message.user("Who is Charlie?"),
        Message.assistant("Charlie is a Golden Retriever."),
    ]
    query = "What color is Charlie?"

    synthesizer = ResponseSynthesizer.preset.stuff(
        model_id="openai/gpt-5-nano",
        system_template="You are a helpful assistant.",
        user_template="{query}",
    )
    response = await synthesizer.synthesize(query=query, history=history)
    print(f"Response: {response}")


if __name__ == "__main__":
    asyncio.run(main())
