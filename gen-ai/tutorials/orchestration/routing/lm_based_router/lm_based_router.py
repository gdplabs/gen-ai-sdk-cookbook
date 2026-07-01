import asyncio
from gllm_inference.request_processor import build_lm_request_processor
from gllm_pipeline.router import LMBasedRouter

# Create an LM request processor
lm_processor = build_lm_request_processor(
    lm_invoker_kwargs={
        "model_id": "openai/gpt-5-nano",
        "credentials": "<YOUR_OPENAI_API_KEY>"
    },
    prompt_builder_kwargs={
        "system_template": "You are a customer support routing assistant.",
        "user_template": "Route this query to the appropriate department: {source}"
    }
)
