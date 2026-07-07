import asyncio

from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM
from gllm_inference.prompt_builder import PromptBuilder
from gllm_inference.request_processor import LMRequestProcessor
from gllm_inference.schema import Message


async def main() -> None:
    history = [
        Message.user("What is the capital city of Indonesia?"),
        Message.assistant("Jakarta is the capital city of Indonesia."),
    ]
    prompt_builder = PromptBuilder(user_template="In what island is it located?")
    lm_invoker = OpenAILMInvoker(OpenAILM.GPT_5_NANO)
    try:
        lm_request_processor = LMRequestProcessor(prompt_builder, lm_invoker)
        output = await lm_request_processor.process(history=history)
        print(f"Response: {output.text}")
    finally:
        await lm_invoker.release_resources()


if __name__ == "__main__":
    asyncio.run(main())
