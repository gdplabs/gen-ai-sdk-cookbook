import asyncio

from dotenv import load_dotenv
from gllm_inference.em_invoker import OpenAIEMInvoker
from gllm_inference.model import OpenAIEM
from gllm_inference.schema import ContentPolicy, OnViolation, TextConstraint

load_dotenv()


async def main():
    em_invoker = OpenAIEMInvoker(OpenAIEM.TEXT_EMBEDDING_3_SMALL)
    response = await em_invoker.invoke("Hello world!")
    print(f"Vectorized text:\n{response}")

    # Content validation and transformation: truncate text over 2000 chars,
    # reject text under 3 chars.
    content_policy = ContentPolicy(
        text=[
            TextConstraint(max_size=2000),
            TextConstraint(min_size=3, on_violation=OnViolation.RAISE),
        ],
    )
    constrained_invoker = OpenAIEMInvoker(
        OpenAIEM.TEXT_EMBEDDING_3_SMALL,
        content_policy=content_policy,
    )
    long_text = "This is a very long text that exceeds the maximum length..." * 100
    constrained_response = await constrained_invoker.invoke(long_text)
    print(f"Vectorized text:\n{constrained_response}")


if __name__ == "__main__":
    asyncio.run(main())
