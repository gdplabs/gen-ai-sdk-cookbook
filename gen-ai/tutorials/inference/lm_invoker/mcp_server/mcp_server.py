import asyncio
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM
from gllm_inference.schema import NativeTool, NativeToolType

SERVER_URL = "https://mcp.deepwiki.com/mcp"
SERVER_NAME = "deepwiki"

# Option 1: as dictionary
mcp_server_tool = {"type": "mcp_server", "url": SERVER_URL, "name": SERVER_NAME}
# Option 2: as native tool object
mcp_server_tool = NativeTool.mcp_server(url=SERVER_URL, name=SERVER_NAME)

lm_invoker = OpenAILMInvoker(OpenAILM.GPT_5_NANO, tools=[mcp_server_tool])
