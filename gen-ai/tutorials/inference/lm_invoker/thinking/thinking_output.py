"""Read thinking results from an LM output.

GitBook: tutorials/inference/lm-invoker/thinking.md#reading-thinking-output
"""

import asyncio

from dotenv import load_dotenv
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM

load_dotenv()


async def main() -> None:
    """Invoke a thinking-enabled model and print its thinking results."""
    lm_invoker = OpenAILMInvoker(OpenAILM.GPT_5_NANO, thinking=True)
    output = await lm_invoker.invoke("Solve x^2 + 2x + 1 = 0")
    for thinking in output.thinkings:
        print(thinking.thinking)


if __name__ == "__main__":
    asyncio.run(main())
