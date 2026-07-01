from typing import TypedDict
from gllm_pipeline.pipeline import Pipeline
from gllm_pipeline.steps import step

class MonolithicRAGState(TypedDict):
    user_query: str
    processed_query: str
    expanded_query: str
    retrieved_documents: list
    filtered_documents: list
    reranked_documents: list
    selected_documents: list
    context: str
    prompt: str
    generated_response: str
    formatted_response: str
    validated_response: str
    response_metadata: dict
