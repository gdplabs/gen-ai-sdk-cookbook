"""Deep Researcher: Data Store Integration.

Demonstrates integrating a data store to pass files to the deep researcher
component via standardized native tools.

Reference: https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/generation/deep-researcher#data-store-integration
"""

from dotenv import load_dotenv
load_dotenv()

import asyncio
from gllm_core.event import EventEmitter
from gllm_generation.deep_researcher import GoogleDeepResearcher
from gllm_inference.schema import AttachmentStore, NativeTool

store = AttachmentStore(id="fileSearchStores/<fileSearchStoreId>", provider="google")
data_store_tool = NativeTool.data_store([store])

event_emitter = EventEmitter.with_print_handler()
query = "Analyze the <topic> document and present it as a concise report!"


async def main():
    deep_researcher = GoogleDeepResearcher(tools=[data_store_tool])
    await deep_researcher.research(query=query, event_emitter=event_emitter)


if __name__ == "__main__":
    asyncio.run(main())
