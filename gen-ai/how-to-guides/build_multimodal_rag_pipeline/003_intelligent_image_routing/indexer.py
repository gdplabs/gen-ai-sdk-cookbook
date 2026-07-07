async def index_document() -> None:
    ...
    # Step 6 — Inspect: print caption and mermaid chunks before indexing
    caption_chunks = [chunk for chunk, _ in chunk_vectors if chunk.metadata.get("chunk_type") == "caption"]
    mermaid_chunks = [chunk for chunk, _ in chunk_vectors if chunk.metadata.get("chunk_type") == "mermaid"]

    print(f"\nFound {len(caption_chunks)} caption chunk(s):")
    for i, chunk in enumerate(caption_chunks, 1):
        print("=" * 50)
        print(f"  [{i}] {chunk.content}")

    print(f"\nFound {len(mermaid_chunks)} mermaid chunk(s):")
    for i, chunk in enumerate(mermaid_chunks, 1):
        print("=" * 50)
        print(f"  [{i}] {chunk.content}")

    # Step 7 — Index
    await data_store.vector.create_from_vector(chunk_vectors)
    print(f"\nIndexed {len(chunk_vectors)} chunk(s).")
