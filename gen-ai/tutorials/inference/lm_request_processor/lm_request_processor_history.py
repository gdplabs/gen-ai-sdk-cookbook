import asyncio

from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM
from gllm_inference.prompt_builder import PromptBuilder
from gllm_inference.request_processor import LMRequestProcessor
from gllm_inference.schema import Message

history = [
    Message.user("What is the capital city of Indonesia?"),
    Message.assistant("Jakarta is the capital city of Indonesia."),
]
prompt_builder = PromptBuilder(user_template="In what island is it located?")
lm_invoker = OpenAILMInvoker(OpenAILM.GPT_5_NANO)
lm_request_processor = LMRequestProcessor(prompt_builder, lm_invoker)
output = asyncio.run(lm_request_processor.process(history=history))
print(f"Response: {output.text}")
