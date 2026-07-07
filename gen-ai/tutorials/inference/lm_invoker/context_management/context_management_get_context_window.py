import asyncio

from gllm_inference.lm_invoker import AnthropicLMInvoker


async def main() -> None:
    lm_invoker = AnthropicLMInvoker("claude-sonnet-4-5")
    try:
        context_window = await lm_invoker.get_context_window()
        print(f"max_input_tokens: {context_window.max_input_tokens}")
        print(f"max_output_tokens: {context_window.max_output_tokens}")
    finally:
        await lm_invoker.release_resources()


if __name__ == "__main__":
    asyncio.run(main())
