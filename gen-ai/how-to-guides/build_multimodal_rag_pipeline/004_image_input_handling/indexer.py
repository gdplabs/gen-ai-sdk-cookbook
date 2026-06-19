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
    """Resize an image so its total pixel count falls within Voyage's range [50k, 1.5M].

    Args:
        image_bytes (bytes): Raw image bytes in any PIL-supported format.

    Returns:
        bytes: The original bytes unchanged if already in range, otherwise
            LANCZOS-rescaled bytes in the same format (PNG fallback if format
            cannot be determined).
    """
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

    def __call__(self, docs: list) -> list:
        """Encode a batch of documents, resizing any image inputs before embedding.

        Args:
            docs (list): Documents to encode — may be raw ``bytes`` or
                ``Attachment`` instances.

        Returns:
            list: Encoded vectors from the parent EMInvokerEncoder.
        """
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
    """Filter metadata to only scalar values supported by ChromaDB.

    Args:
        metadata (dict): Raw metadata dict that may contain non-scalar values.

    Returns:
        dict: A new dict containing only keys whose values are str, int, float, or bool.
    """
    return {k: v for k, v in metadata.items() if isinstance(v, str | int | float | bool)}


def _section_key(el: dict) -> tuple:
    """Return a hashable key representing the section an element belongs to.

    The key is built from all metadata fields whose names start with ``title``,
    sorted alphabetically, so elements that share the same heading hierarchy
    map to the same key.

    Args:
        el (dict): Structured element dict containing a ``metadata`` sub-dict.

    Returns:
        tuple: Title-level metadata values, suitable for use as a dict key.
    """
    metadata = el.get("metadata", {})
    return tuple(
        metadata[k]
        for k in sorted(metadata)
        if k.startswith("title")
    )


def _build_section_texts(elements: list[dict]) -> dict[tuple, str]:
    """Collect and concatenate non-image text per section.

    Args:
        elements (list[dict]): List of structured element dicts from StructuredElementChunker.

    Returns:
        dict[tuple, str]: A dict mapping each section key to the concatenated text of
            all non-image elements in that section, joined by double newlines.
    """
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
    """Convert a single document element into one or more (Chunk, Vector) pairs.

    Text elements produce a single pair. Image elements produce two pairs: one for
    the contextual caption (embedded via text model) and one for the raw image
    (embedded via multimodal model). The router selects the appropriate transformer
    (caption vs. Mermaid) based on image type.

    Args:
        el (dict): Structured element dict as produced by StructuredElementChunker,
            containing keys such as ``structure``, ``text``, and ``metadata`` (which
            may hold a ``media`` list with base64-encoded image content).
        text_description (str, optional): Surrounding section text used as context
            when captioning images. Defaults to "".

    Returns:
        list[tuple[Chunk, Vector]]: (Chunk, Vector) pairs ready to be written to the
            vector store. Empty list if the element is an image with no media content.
    """
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
    """Load, parse, chunk, and index the NARP Operational Guide PDF with smart routing.

    Runs the full ingestion pipeline: load PDF → parse structure → chunk elements →
    build per-section text context → route each image to the appropriate transformer
    (caption or Mermaid) → embed → write to ChromaDB. Prints the number of indexed
    chunks on completion.
    """
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
