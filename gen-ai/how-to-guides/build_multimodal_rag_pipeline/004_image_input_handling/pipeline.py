"""Example script to search by image in a multimodal RAG pipeline.

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/guides/build-multimodal-rag-pipeline/search-by-image
"""

import asyncio
import os
from typing import Any

from dotenv import load_dotenv
from gllm_datastore.data_store import ChromaDataStore
from gllm_datastore.data_store.chroma.data_store import ChromaClientType
from gllm_pipeline.pipeline.states import RAGState
from gllm_generation.response_synthesizer import ResponseSynthesizer
from gllm_inference.em_invoker import VoyageEMInvoker
from gllm_multimodal.modality_converter.image_to_text.image_to_caption import LMBasedImageToCaption
from gllm_pipeline.steps import step, transform
from gllm_retrieval.retriever import VectorRetriever

load_dotenv()

class ImageSearchByImageState(RAGState):
    """RAG state with image bytes functionality.

    Extends the base RAGState to include image bytes.
    """
    image_path: str

# Create components
em_invoker = VoyageEMInvoker(os.getenv("EMBEDDING_MODEL"))
data_store = ChromaDataStore(
    collection_name="narp-operational-guide",
    client_type=ChromaClientType.PERSISTENT,
    persist_directory="data",
).with_vector(em_invoker=em_invoker)
retriever = VectorRetriever(data_store)
response_synthesizer = ResponseSynthesizer.preset.stuff(os.getenv("LANGUAGE_MODEL"))
caption_converter = LMBasedImageToCaption.from_preset("default")


async def build_multimodal_query(state: dict[str, Any]) -> str:
    """Caption the input image and append it to the user query as context.

    Args:
        state (dict[str, Any]): Pipeline state containing ``image_path`` (path to the
            image file) and ``user_query`` (str) keys.

    Returns:
        str: The user query with an image context annotation appended.
    """
    result = await caption_converter.convert(state["image_path"])
    return f"{state["user_query"]}\n\n[Image context: {result.result}]"

# Build the pipeline
caption_step = transform(
    operation=build_multimodal_query,
    input_map={"image_path": "image_path", "user_query": "user_query"},
    output_state="user_query",
)
retrieve_step = step(
    component=retriever,
    input_map={"query": "user_query", "top_k": "top_k"},
    output_state="chunks",
)
synthesize_step = step(
    component=response_synthesizer,
    input_map={"query": "user_query", "chunks": "chunks"},
    output_state="response",
)
e2e_pipeline = caption_step | retrieve_step | synthesize_step
e2e_pipeline.state_type = ImageSearchByImageState


# Run the pipeline
async def main() -> None:
    """Run the image-input RAG pipeline against a sample patient assessment form.

    Invokes the end-to-end pipeline with a hard-coded image path and query, then
    prints the synthesized response to stdout.
    """
    state = ImageSearchByImageState(
        user_query="Which NARP pathway and team should be assigned to this patient?",
        image_path="data/patient_assessment_form.png",
    )
    config = {"top_k": 5}
    result = await e2e_pipeline.invoke(state, config)
    print(f"Pipeline result: {result['response']}")


if __name__ == "__main__":
    asyncio.run(main())
