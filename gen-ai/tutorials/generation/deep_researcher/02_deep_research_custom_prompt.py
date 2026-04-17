from dotenv import load_dotenv
load_dotenv()

import asyncio
from gllm_core.event import EventEmitter
from gllm_inference.prompt_builder import PromptBuilder
from gllm_generation.deep_researcher import OpenAIDeepResearcher

prompt_builder = PromptBuilder(
    system_template="Perform your deep research as if you are a rapper.",
    user_template="{query}",
)

query = "Create a concise report about why bananas are yellow."
event_emitter = EventEmitter.with_print_handler()

async def main():
    deep_researcher = OpenAIDeepResearcher(prompt_builder=prompt_builder)
    await deep_researcher.research(query=query, event_emitter=event_emitter)

if __name__ == "__main__":
    asyncio.run(main())
