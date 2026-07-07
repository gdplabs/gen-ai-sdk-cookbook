import asyncio

from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM
from gllm_inference.prompt_builder import PromptBuilder
from gllm_inference.request_processor import LMRequestProcessor


async def main() -> None:
    role = "pirate"
    query = "What is the capital city of Indonesia?"

    prompt_builder = PromptBuilder(system_template="Talk like a {role}.", user_template="{query}")
    lm_invoker = OpenAILMInvoker(OpenAILM.GPT_5_NANO)
    try:
        lm_request_processor = LMRequestProcessor(prompt_builder, lm_invoker)
        output = await lm_request_processor.process(role=role, query=query)
        print(f"Response: {output.text}")
    finally:
        await lm_invoker.release_resources()


if __name__ == "__main__":
    asyncio.run(main())
