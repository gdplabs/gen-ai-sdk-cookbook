from dotenv import load_dotenv
load_dotenv()

import asyncio
from gllm_core.event import EventEmitter
from gllm_inference.schema import NativeTool
from gllm_generation.deep_researcher import OpenAIDeepResearcher

mcp_server = NativeTool.mcp_server(name="...", url="https://.../mcp")
mcp_connector = NativeTool.mcp_connector(
    name="google_drive",
    connector_id="connector_googledrive",
    auth="<google_oauth_token>",
)

event_emitter = EventEmitter.with_print_handler()
query = "Create a concise report about my Google Drive structure!"

deep_researcher = OpenAIDeepResearcher(tools=[mcp_server, mcp_connector])
asyncio.run(deep_researcher.research(query=query, event_emitter=event_emitter))
