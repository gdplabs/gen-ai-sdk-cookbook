"""Example script to index a mixed set of images (photos + diagrams) using smart routing
with contextual captions enriched by surrounding section text.

Authors:
    Nico Samuelson Tjandra (nico.s.tjandra@gdplabs.id)

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/guides/build-multimodal-rag-pipeline/smart-image-routing
"""

import asyncio
import base64
import io
import os

from dotenv import load_dotenv
from gllm_core.retry import RetryConfig
from gllm_core.schema import Chunk
from gllm_datastore.data_store import ChromaDataStore
from gllm_datastore.data_store.chroma.data_store import ChromaClientType
from gllm_docproc.chunker.structured_element import StructuredElementChunker
from gllm_docproc.loader.pdf import PyMuPDFLoader
from gllm_docproc.model.element import IMAGE
from gllm_docproc.parser.document import PDFParser
from gllm_inference.em_invoker import VoyageEMInvoker
from gllm_inference.schema import Attachment, Vector
from gllm_multimodal.modality_transformer.image_modality_transformer.standard_image_modality_transformer import (
    StandardImageModalityTransformer,
)
from gllm_multimodal.modality_transformer.image_modality_transformer.standard_image_modality_transformer.preset import LMBasedImageToCaption, LMBasedImageToMermaid
from gllm_pipeline.router.aurelio_semantic_router import AurelioSemanticRouter
from gllm_pipeline.router.backend.aurelio.encoders.em_invoker_encoder import EMInvokerEncoder
from PIL import Image

load_dotenv()

_VOYAGE_MIN_PIXELS = 50_001
_VOYAGE_MAX_PIXELS = 1_500_000


def _clamp_image_pixels(image_bytes: bytes) -> bytes:
    """Resize image to fit within Voyage's permitted pixel range [50k, 2M]."""
    img = Image.open(io.BytesIO(image_bytes))
    w, h = img.size
    total = w * h
    if _VOYAGE_MIN_PIXELS <= total <= _VOYAGE_MAX_PIXELS:
        return image_bytes
    target = _VOYAGE_MIN_PIXELS if total < _VOYAGE_MIN_PIXELS else _VOYAGE_MAX_PIXELS
    scale = (target / total) ** 0.5
    new_w = max(int(w * scale), 1)
    new_h = max(int(h * scale), 1)
    print(f"Resizing image from {w}x{h} to {new_w}x{new_h}")
    img = img.resize((new_w, new_h), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format=img.format or "PNG")
    return buf.getvalue()


class _ResizingEncoder(EMInvokerEncoder):
    """Wraps EMInvokerEncoder to resize images into Voyage's permitted pixel range.

    The router preset prepares each utterance as an Attachment (via Attachment.from_url),
    so we unwrap .data, resize, and rebuild the Attachment rather than expecting raw bytes.
    """

    def __call__(self, docs):
        resized = []
        for doc in docs:
            if isinstance(doc, bytes):
                doc = _clamp_image_pixels(doc)
            elif isinstance(doc, Attachment) and doc.data:
                doc = Attachment.from_bytes(_clamp_image_pixels(doc.data), filename=doc.filename)
            resized.append(doc)
        return super().__call__(resized)

em_invoker = VoyageEMInvoker(os.getenv("EMBEDDING_MODEL"))
data_store = ChromaDataStore(
    collection_name="narp-operational-guide",
    client_type=ChromaClientType.PERSISTENT,
    persist_directory="data",
).with_vector(em_invoker=em_invoker)

encoder = _ResizingEncoder(em_invoker=em_invoker)
retry_config = RetryConfig(
    max_retries=3,
    timeout=120
)
caption_converter = LMBasedImageToCaption.from_preset("default", lm_invoker_kwargs={"config": {"retry_config": retry_config}})
mermaid_converter = LMBasedImageToMermaid.from_preset("default", lm_invoker_kwargs={"config": {"retry_config": retry_config}})

router = AurelioSemanticRouter.from_preset(
    modality="image",
    preset_name="multimodal",
    preset_kwargs={"encoder": encoder}
)
transformer = StandardImageModalityTransformer(
    router=router,
    route_mapping={
        "chart": caption_converter,
        "data_visualization": caption_converter,
        "document": caption_converter,
        "engineering_drawing": caption_converter,
        "general_image": caption_converter,
        "grid_diagram": caption_converter,
        "mechanical_part": caption_converter,
        "presentation": caption_converter,
        "scientific_diagram": caption_converter,
        "scientific_figure": caption_converter,
        "table": caption_converter,
        "diagram": mermaid_converter,
        "organization_chart": mermaid_converter,
    }
)


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
    if el.get("structure", "uncategorized") != IMAGE:
        el["metadata"]["structure"] = el.get("structure", "uncategorized")
        chunk = Chunk(content=el.get("text", ""), metadata=_scalar_metadata(el.get("metadata", {})))
        vector = await em_invoker.invoke(chunk.content)
        return [(chunk, vector)]

    metadata = el.get("metadata", {})
    media = metadata.get("media", [])
    if not media:
        return []
    image_bytes = _clamp_image_pixels(base64.b64decode(media[0].get("media_content", "")))

    # Pass section text as text_context so the LM generates contextually grounded captions
    result = await transformer.transform(image_bytes, text_context=text_description)
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
    loaded_elements = loader.load("./data/NARP-Operational-Guide-trimmed.pdf")

    # Step 2 — Parse: assign structural roles (heading, paragraph, image, …)
    parser = PDFParser()
    parsed_elements = parser.parse(loaded_elements)

    # Step 3 — Chunk: group elements; pass excluded_structures=[] to keep IMAGE elements
    chunker = StructuredElementChunker()
    chunked_elements = chunker.chunk(parsed_elements, excluded_structures=[])

    # Step 4 — Build a section-text lookup so each image gets its surrounding article text
    section_texts = _build_section_texts(chunked_elements)

    # Step 5 — Caption and embed all elements concurrently
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
