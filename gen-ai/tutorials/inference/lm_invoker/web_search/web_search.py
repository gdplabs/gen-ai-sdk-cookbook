import asyncio
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM
from gllm_inference.schema import NativeTool, NativeToolType

# Option 1: as string
web_search_tool = "web_search"
# Option 2: as enum
web_search_tool = NativeToolType.WEB_SEARCH
# Option 3: as dictionary (useful for providing custom kwargs)
web_search_tool = {"type": "web_search", **kwargs}
# Option 4: as native tool object (useful for providing custom kwargs)
web_search_tool = NativeTool.web_search(**kwargs)

lm_invoker = OpenAILMInvoker(OpenAILM.GPT_5_NANO, tools=[web_search_tool])
