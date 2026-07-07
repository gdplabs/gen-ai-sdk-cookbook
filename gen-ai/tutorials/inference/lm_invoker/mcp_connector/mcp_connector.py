import asyncio
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM
from gllm_inference.schema import NativeTool

# Create Google Drive MCP connector
google_drive_connector = NativeTool.mcp_connector(
    connector_id="connector_googledrive",
    name="google_drive",
    auth="<your_google_oauth_token>",
)

# Initialize LM invoker with the connector
lm_invoker = OpenAILMInvoker(
    OpenAILM.GPT_5_NANO,
    tools=[google_drive_connector]
)

# Query that requires Google Drive access
query = "List all PDF files in my Google Drive that were modified in the last week"
output = asyncio.run(lm_invoker.invoke(query))

# Access MCP connector calls
for item in output.outputs:
    print(f"=== Output item: {item.type!r} ===\n{item.output}\n")
