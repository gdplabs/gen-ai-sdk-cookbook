import asyncio
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM
from gllm_inference.output_transformer import OutputTransformerConfig

output_transformers = [
    # Option 1: as string
    "identity",
    # Option 2: as dictionary
    {"type": "json"},
    # Option 3: as config object
    OutputTransformerConfig.think_tag(),
    # Option 4: as config object with kwargs
    OutputTransformerConfig.validation({"structured"}),
    # Option 5: as config object with kwargs
    OutputTransformerConfig.event_filter(["thinking"]),
]

lm_invoker = OpenAILMInvoker(
    OpenAILM.GPT_5_NANO,
    output_transformers=output_transformers,
)
