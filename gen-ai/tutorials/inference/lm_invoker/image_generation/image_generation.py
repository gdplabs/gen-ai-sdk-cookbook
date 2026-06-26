import asyncio
from gllm_core.retry import RetryConfig
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM
from gllm_inference.schema import NativeTool, NativeToolType

# Option 1: as string
image_generation_tool = "image_generation"
# Option 2: as enum
image_generation_tool = NativeToolType.IMAGE_GENERATION
# Option 3: as dictionary (useful for providing custom kwargs)
image_generation_tool = {"type": "image_generation", **kwargs}
# Option 4: as native tool object (useful for providing custom kwargs)
image_generation_tool = NativeTool.image_generation(**kwargs)

retry_config = RetryConfig(timeout=60)
lm_invoker = OpenAILMInvoker(
    OpenAILM.GPT_5_NANO, 
    tools=[image_generation_tool], 
    retry_config=retry_config,
)
