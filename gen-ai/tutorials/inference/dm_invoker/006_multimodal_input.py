"""006: Evaluate an image with a Decision Model (DM) invoker.

GitBook: https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/inference/dm-invoker#multimodal-input
"""

import asyncio

from dotenv import load_dotenv
from gllm_inference.dm_invoker import OpenAIDMInvoker
from gllm_inference.schema import Attachment, DMQuestion


async def main() -> None:
    """Ask whether an attached image shows a dog."""
    load_dotenv()
    image = Attachment.from_path("path/to/dog.jpeg")
    invoker = OpenAIDMInvoker(model_name="gpt-6-luna")
    try:
        result = await invoker.invoke(
            state=["Analyze the attached image.", image],
            questions={
                "is_dog": DMQuestion.noul(
                    instructions="Does the image show a dog?",
                ),
            },
        )
        print(result.answers["is_dog"].noul)
    finally:
        await invoker.release_resources()


if __name__ == "__main__":
    asyncio.run(main())
