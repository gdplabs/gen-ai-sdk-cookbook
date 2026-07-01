import asyncio
from gllm_inference.em_invoker import build_em_invoker

# Create an embedding model invoker
em_invoker = build_em_invoker(
    "openai/text-embedding-3-small",
    credentials={"api_key": "<YOUR_OPENAI_API_KEY>"}
)
