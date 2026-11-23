"""Response Synthesizer: Passing a Custom LM Invoker.

Demonstrates building an LM invoker and passing it to the stuff() method.

References:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/generation/response-synthesizer#passing-a-custom-lm-invoker
"""

import asyncio

from dotenv import load_dotenv

from gllm_generation.response_synthesizer import ResponseSynthesizer
from gllm_inference.lm_invoker import build_lm_invoker

load_dotenv()


async def main() -> None:
    """Synthesize a response using a custom LM invoker."""
    lm_invoker = build_lm_invoker(model_id="openai/gpt-5-nano")
    lm_invoker.prompt.build(
        system_template="Talk like a pirate.",
        user_template="Name an animal that starts with the letter 'A'!",
    )

    synthesizer = ResponseSynthesizer.stuff(lm_invoker=lm_invoker)
    response = await synthesizer.synthesize()
    print(f"Response: {response}")


if __name__ == "__main__":
    asyncio.run(main())
