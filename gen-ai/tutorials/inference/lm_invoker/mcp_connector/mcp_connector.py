import asyncio
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM
from gllm_inference.schema import NativeTool, OAuthCredentials

# Option 1: Using dictionary
mcp_connector_tool = {
    "type": "mcp_connector",
    "connector_id": "connector_googledrive",
    "name": "google_drive",
    "auth": "<google_oauth_token>",
}

# Option 2: Using NativeTool factory method (recommended)
mcp_connector_tool = NativeTool.mcp_connector(
    connector_id="connector_googledrive",
    name="google_drive",
    auth="<google_oauth_token>",
)

lm_invoker = OpenAILMInvoker(OpenAILM.GPT_5_NANO, tools=[mcp_connector_tool])
