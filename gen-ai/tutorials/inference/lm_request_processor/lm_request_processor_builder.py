import os

from gllm_inference.request_processor import build_lm_request_processor

# Simple LMRP creation with essential parameters
lm_request_processor = build_lm_request_processor(
    model_id="openai/gpt-5-nano",
    credentials=os.getenv("OPENAI_API_KEY"),
    system_template="You are a helpful assistant that provides accurate information.",
    user_template="Please answer this question: {question}",
)
