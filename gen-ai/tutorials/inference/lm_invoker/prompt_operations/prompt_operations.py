import asyncio

from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM
from gllm_inference.schema import Message


async def main() -> None:
    lm_invoker = OpenAILMInvoker(OpenAILM.GPT_5_NANO)
    lm_invoker.prompt.build(
        system_template="You are a helpful coding assistant.",
        user_template="Summarize this bug report in 3 bullets: {report}",
    )

    history = [
        Message.user("My name is Rina."),
        Message.assistant("Nice to meet you, Rina."),
    ]

    output = await lm_invoker.prompt.invoke(
        history=history,
        report="What is my name?",
    )
    print(output.text)


if __name__ == "__main__":
    asyncio.run(main())
