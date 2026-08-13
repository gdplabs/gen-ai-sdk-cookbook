import asyncio

from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM
from gllm_inference.prompt_builder import PromptBuilder
from gllm_inference.request_processor import LMRequestProcessor


async def main() -> None:
    prompt_builder = PromptBuilder(
        system_template="Talk like a pirate.",
        user_template="What is the capital city of Indonesia?",
    )
    lm_invoker = OpenAILMInvoker(OpenAILM.GPT_5_NANO)
    lm_request_processor = LMRequestProcessor(prompt_builder, lm_invoker)
    output = await lm_request_processor.process()
    print(f"Response: {output.text}")


if __name__ == "__main__":
    asyncio.run(main())
