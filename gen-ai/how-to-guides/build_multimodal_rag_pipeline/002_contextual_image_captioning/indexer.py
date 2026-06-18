"""Example script to index images with contextual captions extracted from a PDF.

Authors:
    Nico Samuelson Tjandra (nico.s.tjandra@gdplabs.id)

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/guides/build-multimodal-rag-pipeline/image-search-pipeline
"""

import asyncio
import base64
import os

from dotenv import load_dotenv
from gllm_core.schema import Chunk
from gllm_datastore.data_store import ChromaDataStore
from gllm_datastore.data_store.chroma.data_store import ChromaClientType
from gllm_docproc.chunker.structured_element import StructuredElementChunker
from gllm_docproc.loader.pdf import PyMuPDFLoader
from gllm_docproc.model.element import IMAGE
from gllm_docproc.parser.document import PDFParser
from gllm_inference.em_invoker import VoyageEMInvoker
from gllm_inference.schema import Attachment, Vector
from gllm_multimodal.modality_converter.image_to_text.image_to_caption import LMBasedImageToCaption

load_dotenv()

# Initialize vector store
em_invoker = VoyageEMInvoker(os.getenv("EMBEDDING_MODEL"))
data_store = ChromaDataStore(
    collection_name="indonesia-tourism-contextual",
    client_type=ChromaClientType.PERSISTENT,
    persist_directory="data",
).with_vector(em_invoker=em_invoker)

caption_converter = LMBasedImageToCaption.from_preset("default")


def _scalar_metadata(metadata: dict) -> dict:
    return {k: v for k, v in metadata.items() if isinstance(v, str | int | float | bool)}


def _section_key(el: dict) -> tuple:
    """Return a hashable key representing the section an element belongs to."""
    metadata = el.get("metadata", {})

    return tuple(
        metadata[k]
        for k in sorted(metadata)
        if k.startswith("title")
    )


def _build_section_texts(elements: list[dict]) -> dict[tuple, str]:
    """Collect and concatenate non-image text per section."""
    texts: dict[tuple, list[str]] = {}
    for el in elements:
        if el.get("structure", "uncategorized") == IMAGE:
            continue
        text = el.get("text", "").strip()
        if not text:
            continue
        key = _section_key(el)
        texts.setdefault(key, []).append(text)
    return {key: "\n\n".join(parts) for key, parts in texts.items()}


async def process_element(el: dict, text_description: str = "") -> list[tuple[Chunk, Vector]]:
    # Non-image elements are processed as text chunks
    if el.get("structure", "uncategorized") != IMAGE:
        el["metadata"]["structure"] = el.get("structure", "uncategorized")
        chunk = Chunk(content=el.get("text", ""), metadata=_scalar_metadata(el.get("metadata", {})))
        vector = await em_invoker.invoke(chunk.content)
        return [(chunk, vector)]

    metadata = el.get("metadata", {})
    media = metadata.get("media", [])
    if not media:
        return []
    image_bytes = base64.b64decode(media[0].get("media_content", ""))

    # Pass section text as text_context so the LM generates contextually grounded captions
    result = await caption_converter.convert(
        image_bytes, 
        text_context=text_description # Article context is added here
    )
    metadata["structure"] = el["structure"]
    scalar_meta = _scalar_metadata(metadata)

    # Image element will be stored as both caption and image chunks
    caption_chunk = Chunk(content=result.result, metadata=scalar_meta)
    image_chunk = Chunk(content=result.result, metadata=scalar_meta)
    caption_vector, image_vector = await asyncio.gather(
        em_invoker.invoke(result.result),
        em_invoker.invoke(Attachment.from_bytes(image_bytes)),
    )
    return [(caption_chunk, caption_vector), (image_chunk, image_vector)]


async def index_document() -> None:
    # Step 1 — Load: extract text and images (as base64) from the PDF
    loader = PyMuPDFLoader()
    loaded_elements = loader.load("./data/indonesia_tourism.pdf")

   # Step 2 — Parse: assign structural roles (heading, paragraph, image, …)
    parser = PDFParser()
    parsed_elements = parser.parse(loaded_elements)

    # Step 3 — Chunk: group elements; pass excluded_structures=[] to keep IMAGE elements
    chunker = StructuredElementChunker()
    chunked_elements = chunker.chunk(parsed_elements, excluded_structures=[])

    # Step 4 — Build a section-text lookup so each image gets its surrounding article text
    section_texts = _build_section_texts(chunked_elements)

    # Step 5 — Process all elements concurrently
    results = await asyncio.gather(*[
        process_element(el, text_description=section_texts.get(_section_key(el), ""))
        for el in chunked_elements
    ])
    chunk_vectors = [pair for element_pairs in results for pair in element_pairs]

    # Step 6 — Index
    await data_store.vector.create_from_vector(chunk_vectors)
    print(f"\nIndexed {len(chunk_vectors)} chunks.")


if __name__ == "__main__":
    asyncio.run(index_document())
