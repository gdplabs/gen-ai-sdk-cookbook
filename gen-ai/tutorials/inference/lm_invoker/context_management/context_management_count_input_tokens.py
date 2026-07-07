import asyncio

from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM
from gllm_inference.schema import Message

lm_invoker = OpenAILMInvoker(OpenAILM.GPT_5_NANO)

messages = [
    Message.system("You are a helpful assistant."),
    Message.user("Summarize this paragraph in one sentence."),
]

input_tokens = asyncio.run(lm_invoker.count_input_tokens(messages))
print(f"input_tokens: {input_tokens}")
