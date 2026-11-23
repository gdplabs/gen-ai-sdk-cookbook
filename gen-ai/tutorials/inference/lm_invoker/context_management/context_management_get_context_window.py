import asyncio

from gllm_inference.lm_invoker import AnthropicLMInvoker


async def main() -> None:
    lm_invoker = AnthropicLMInvoker("claude-sonnet-4-5")
    context_window = await lm_invoker.get_context_window()
    print(f"max_input_tokens: {context_window.max_input_tokens}")
    print(f"max_output_tokens: {context_window.max_output_tokens}")


if __name__ == "__main__":
    asyncio.run(main())
