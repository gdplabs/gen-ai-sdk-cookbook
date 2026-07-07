from gllm_inference.request_processor import build_lm_request_processor
from gllm_generation.response_synthesizer.strategy import RefineSynthesisStrategy
from gllm_generation.response_synthesizer import ResponseSynthesizer

# Custom prompt for refinement
processor = build_lm_request_processor(
    model_id="openai/gpt-5",
    system_template="You are a helpful assistant that refines answers based on new information.",
    user_template="""Query: {query}

Current Answer:
{draft_response}

New Information:
{context}

Refine the current answer by incorporating the new information. If the new information contradicts the current answer, update it accordingly."""
)

strategy = RefineSynthesisStrategy(
    lm_request_processor=processor,
    batch_size=2,  # Process 2 chunks at a time
    stream_drafts=True  # Stream intermediate drafts
)

synthesizer = ResponseSynthesizer(strategy=strategy)
