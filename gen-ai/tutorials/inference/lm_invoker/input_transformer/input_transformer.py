import asyncio
from gllm_inference.input_transformer import InputTransformerConfig
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM

input_transformers = [
    # Option 1: as string
    "identity",
    # Option 2: as dictionary
    {"type": "filter_empty"},
    # Option 3: as config object
    InputTransformerConfig.filter_empty(),
]

lm_invoker = OpenAILMInvoker(
    OpenAILM.GPT_5_NANO,
    input_transformers=input_transformers,
)
