import asyncio
from gllm_inference.lm_invoker import AnthropicLMInvoker

lm_invoker = AnthropicLMInvoker("claude-sonnet-4-0")

context_window = asyncio.run(lm_invoker.get_context_window())
print(f"max_input_tokens: {context_window.max_input_tokens}")
print(f"max_output_tokens: {context_window.max_output_tokens}")
