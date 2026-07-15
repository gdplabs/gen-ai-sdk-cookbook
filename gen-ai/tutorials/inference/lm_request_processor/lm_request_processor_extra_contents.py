import asyncio

from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM
from gllm_inference.prompt_builder import PromptBuilder
from gllm_inference.request_processor import LMRequestProcessor
from gllm_inference.schema import Attachment


async def main() -> None:
    attachment = Attachment.from_path("path/to/tiger.jpg")
    prompt_builder = PromptBuilder(user_template="What image is this?")
    lm_invoker = OpenAILMInvoker(OpenAILM.GPT_5_NANO)
    try:
        lm_request_processor = LMRequestProcessor(prompt_builder, lm_invoker)
        output = await lm_request_processor.process(extra_contents=[attachment])
        print(f"Response: {output.text}")
    finally:
        await lm_invoker.release_resources()


if __name__ == "__main__":
    asyncio.run(main())
