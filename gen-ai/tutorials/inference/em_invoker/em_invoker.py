import asyncio
from gllm_inference.em_invoker import OpenAIEMInvoker
from gllm_inference.model import OpenAIEM
from gllm_inference.schema.config import TruncationConfig, TruncateSide

# Configure text truncation
truncation_config = TruncationConfig(
    max_length=1000,
    truncate_side=TruncateSide.RIGHT
)

em_invoker = OpenAIEMInvoker(
    OpenAIEM.TEXT_EMBEDDING_3_SMALL,
    truncation_config=truncation_config
)

long_text = "This is a very long text that exceeds the maximum length..." * 100
response = asyncio.run(em_invoker.invoke(long_text))
print(f"Vectorized text:\n{response}")
