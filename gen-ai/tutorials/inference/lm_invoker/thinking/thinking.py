"""Configure thinking, invoke a model, and inspect its reasoning output.

GitBook:
- tutorials/inference/lm-invoker/thinking.md#what-is-thinking
- tutorials/inference/lm-invoker/thinking.md#configuring-thinking
- tutorials/inference/lm-invoker/thinking.md#portable-effort
- tutorials/inference/lm-invoker/thinking.md#reading-thinking-output
"""

import asyncio

from dotenv import load_dotenv
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM
from gllm_inference.schema import ThinkingConfig

load_dotenv()


async def main() -> None:
    """Invoke an OpenAI model with configured thinking and print its reasoning."""
    thinking_config = ThinkingConfig(effort="high", kwargs={"summary": "auto"})
    lm_invoker = OpenAILMInvoker(OpenAILM.GPT_5_NANO, thinking=thinking_config)
    query = "Solve x^2 + 2x + 1 = 0"
    output = await lm_invoker.invoke(query)
    for thinking in output.thinkings:
        print(thinking.thinking)


if __name__ == "__main__":
    asyncio.run(main())
