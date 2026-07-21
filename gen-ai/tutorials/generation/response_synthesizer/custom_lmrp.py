"""Response Synthesizer: Passing Custom LM Request Processor.

Demonstrates passing an LMRequestProcessor object to the stuff() method.

Reference: https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/generation/response-synthesizer#passing-custom-lm-request-processor
"""

import asyncio

from dotenv import load_dotenv

from gllm_inference.request_processor import build_lm_request_processor
from gllm_generation.response_synthesizer import ResponseSynthesizer

load_dotenv()


async def main() -> None:
    lm_request_processor = build_lm_request_processor(
        model_id="openai/gpt-5-nano",
        system_template="Talk like a pirate.",
        user_template="Name an animal that starts with the letter 'A'!",
    )

    synthesizer = ResponseSynthesizer.stuff(lm_request_processor=lm_request_processor)
    response = await synthesizer.synthesize()
    print(f"Response: {response}")


if __name__ == "__main__":
    asyncio.run(main())
