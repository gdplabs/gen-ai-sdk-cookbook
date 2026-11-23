import asyncio

from gllm_inference.lm_invoker import AnthropicLMInvoker
from gllm_inference.schema import Message


async def main() -> None:
    # AnthropicLMInvoker supports both get_context_window() and count_input_tokens(),
    # so it can be used to combine both methods to guard invocations.
    lm_invoker = AnthropicLMInvoker("claude-sonnet-4-5")
    messages = [
        Message.system("You are a helpful assistant."),
        Message.user("Summarize this paragraph in one sentence."),
    ]

    context_window = await lm_invoker.get_context_window()
    input_tokens = await lm_invoker.count_input_tokens(messages)

    if context_window.max_input_tokens and input_tokens > context_window.max_input_tokens:
        raise ValueError("Input exceeds model context window")

    print("Input is within context window limits.")


if __name__ == "__main__":
    asyncio.run(main())
