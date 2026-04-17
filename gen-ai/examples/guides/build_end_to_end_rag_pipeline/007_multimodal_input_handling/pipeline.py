"""Example script to build and run a RAG pipeline with multimodal input handling.

Authors:
    Delfia N.A Putri (delfia.n.a.putri@gdplabs.id)

References:
    [1] https://gdplabs.gitbook.io/sdk/how-to-guides/build-end-to-end-rag-pipeline/multimodal-input-handling
"""

import asyncio
import os
from typing import Any

from dotenv import load_dotenv
from gllm_datastore.vector_data_store import ChromaVectorDataStore
from gllm_generation.response_synthesizer import ResponseSynthesizer
from gllm_inference.builder import build_lm_request_processor
from gllm_inference.em_invoker.openai_em_invoker import OpenAIEMInvoker
from gllm_inference.schema import Attachment, MessageContent
from gllm_pipeline.pipeline.states import RAGState
from gllm_pipeline.steps import step, transform
from gllm_retrieval.retriever.vector_retriever import BasicVectorRetriever

load_dotenv()

class MultimodalRAGState(RAGState):
    """RAG state with multimodal input support.

    Extends the base RAGState to include attachments and extra content for multimodal processing.
    """
    attachments: list[str]
    extra_contents: list[MessageContent]

# Function to format extra contents
def format_extra_contents(inputs: dict[str, Any]) -> list[MessageContent]:
    """Format extra content from attachment paths.

    Args:
        inputs: Dictionary containing attachment paths under 'attachments' key.

    Returns:
        List of MessageContent objects created from the attachment paths.
    """
    attachments: list[bytes] = inputs["attachments"]
    return [Attachment.from_path(path) for path in attachments]


# Create components
em_invoker = OpenAIEMInvoker(os.getenv("EMBEDDING_MODEL"))
data_store = ChromaVectorDataStore(
    collection_name="documents",
    client_type="persistent",
    persist_directory="data",
    embedding=em_invoker,
)
retriever = BasicVectorRetriever(data_store)
response_synthesizer = ResponseSynthesizer.stuff(
    lm_request_processor=build_lm_request_processor(
        model_id=os.getenv("LANGUAGE_MODEL"),
        credentials=os.getenv("OPENAI_API_KEY"),
        system_template="""Create an imaginary animal that is similar to the animal in the picture. Context: {context}""",
        user_template="Question: {query}",
    )
)

# Create the pipeline
format_extra_contents_step = transform(
    format_extra_contents,
    ["attachments"],
    "extra_contents",
)
retrieve_step = step(
    component=retriever,
    input_map={"query": "user_query", "top_k": "top_k"},
    output_state="chunks",
)
synthesize_step = step(
    component=response_synthesizer,
    input_map={"query": "user_query", "chunks": "chunks", "extra_contents": "extra_contents"},
    output_state="response",
)


e2e_pipeline = format_extra_contents_step | retrieve_step | synthesize_step
e2e_pipeline.state_type = MultimodalRAGState

# Run the pipeline
async def main():
    state = {
        "user_query": "Aquatic animals",
        "attachments": ["dog.png"],
    }
    config = {"top_k": 5}
    result = await e2e_pipeline.invoke(state, config)
    print(f"Pipeline result: {result['response']}")


if __name__ == "__main__":
    asyncio.run(main())
