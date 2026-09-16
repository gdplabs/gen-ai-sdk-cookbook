"""Enable thinking and inspect the resulting output items.

GitBook: tutorials/inference/lm-invoker/thinking.md#what-is-thinking
"""

import asyncio

from dotenv import load_dotenv
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM

load_dotenv()


async def main() -> None:
    """Invoke an OpenAI model with thinking enabled."""
    lm_invoker = OpenAILMInvoker(OpenAILM.GPT_5_NANO, thinking=True)
    query = "Solve x^2 + 2x + 1 = 0"
    output = await lm_invoker.invoke(query)
    for item in output.outputs:
        print(f"=== Output item: {item.type!r} ===\n{item.output}\n")


if __name__ == "__main__":
    asyncio.run(main())
