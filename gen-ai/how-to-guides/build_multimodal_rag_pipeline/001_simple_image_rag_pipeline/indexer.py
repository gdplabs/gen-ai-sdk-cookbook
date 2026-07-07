def _scalar_metadata(metadata: dict) -> dict:
    return {k: v for k, v in metadata.items() if isinstance(v, str | int | float | bool)}


async def process_element(el: dict) -> list[tuple[Chunk, Vector]]:
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
    result = await caption_converter.convert(image_bytes)
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


async def index_document():
    # Step 1 — Load: extract text and images from the PDF
    loader = PyMuPDFLoader()
    loaded_elements = loader.load("./data/indonesia_tourism.pdf")

    # Step 2 — Parse: assign structural roles (heading, paragraph, image, …)
    parser = PDFParser()
    parsed_elements = parser.parse(loaded_elements)

    # Step 3 — Chunk: group elements
    chunker = StructuredElementChunker()
    chunked_elements = chunker.chunk(parsed_elements, excluded_structures=[])

    # Step 4 — Process all elements concurrently
    results = await asyncio.gather(*[process_element(el) for el in chunked_elements])
    chunk_vectors = [pair for element_pairs in results for pair in element_pairs]

    # Step 5 — Inspect: print image caption chunks before indexing
    caption_chunks = [chunk for chunk, _ in chunk_vectors if chunk.metadata.get("chunk_type") == "caption"]
    print(f"\nFound {len(caption_chunks)} image caption chunk(s):")
    for i, chunk in enumerate(caption_chunks, 1):
        print("=" * 50)
        print(f"  [{i}] {chunk.content}")

    # Step 6 — Index
    await data_store.vector.create_from_vector(chunk_vectors)
    print(f"\nIndexed {len(chunk_vectors)} chunk(s).")


if __name__ == "__main__":
    asyncio.run(index_document())
