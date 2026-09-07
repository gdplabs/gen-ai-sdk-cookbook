import asyncio

from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM
from gllm_inference.schema import ContentPolicy, OnViolation, TextConstraint


async def main() -> None:
    # Content validation and transformation: truncate text over 4000 chars,
    # reject text under 3 chars.
    content_policy = ContentPolicy(
        text=[
            TextConstraint(max_size=4000),
            TextConstraint(min_size=3, on_violation=OnViolation.RAISE),
        ],
    )

    lm_invoker = OpenAILMInvoker(
        OpenAILM.GPT_5_NANO,
        content_policy=content_policy,
    )

    output = await lm_invoker.invoke("What is the capital city of Indonesia?")
    print(f"output: {output.text}")

    long_text = "This is a very long text that exceeds the maximum length..." * 200
    transformed_output = await lm_invoker.invoke(long_text)
    print(f"transformed output: {transformed_output.text}")

    await lm_invoker.release_resources()


if __name__ == "__main__":
    asyncio.run(main())