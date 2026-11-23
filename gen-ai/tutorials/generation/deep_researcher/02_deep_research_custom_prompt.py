"""Deep Researcher: Custom Prompt using PromptBuilder.

Demonstrates customizing the deep researcher prompts by supplying a custom
PromptBuilder object.

Reference: https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/generation/deep-researcher#custom-prompt
"""

from dotenv import load_dotenv
load_dotenv()

import asyncio
from gllm_core.event import EventEmitter
from gllm_inference.prompt_builder import PromptBuilder
from gllm_generation.deep_researcher import OpenAIDeepResearcher

prompt_builder = PromptBuilder(
    system_template=(
        "Provide your deep research results as if you are a journalist "
        "writing a news article."
    ),
    user_template="{query}",
)
event_emitter = EventEmitter.with_print_handler()
query = "Create a concise report about why bananas are yellow."


async def main():
    deep_researcher = OpenAIDeepResearcher(prompt_builder=prompt_builder)
    await deep_researcher.research(query=query, event_emitter=event_emitter)


if __name__ == "__main__":
    asyncio.run(main())
