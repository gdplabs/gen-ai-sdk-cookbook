"""
Combining query filter conditions with AND, OR, NOT logic.

Reference:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/data-store/query-filter#combining-conditions-flat-and
"""

import asyncio

from dotenv import load_dotenv
from gllm_core.schema import Chunk
from gllm_datastore.core.filters import QueryOptions, filter as F
from gllm_datastore.data_store import ChromaDataStore
from gllm_datastore.data_store.chroma.data_store import ChromaClientType
from gllm_inference.em_invoker import OpenAIEMInvoker

load_dotenv()


async def main() -> None:
    """Combine multiple filter clauses with and_, or_, and not_."""
    em_invoker = OpenAIEMInvoker(model_name="text-embedding-3-small")
    store = (
        ChromaDataStore(
            collection_name="customer-notes",
            client_type=ChromaClientType.MEMORY,
        )
        .with_fulltext()
        .with_vector(em_invoker=em_invoker)
    )

    chunks = [
        Chunk(
            id="book:1",
            content="AI is useful for programming",
            metadata={"topic": "AI", "category": "published"},
        ),
        Chunk(
            id="book:2",
            content="Cheesecake is delicious",
            metadata={"topic": "food", "category": "published"},
        ),
        Chunk(
            id="book:3",
            content="Sushi is delicious",
            metadata={"topic": "food", "category": "unpublished"},
        ),
    ]
    await store.fulltext.create(chunks)

    # Combining conditions (flat AND)
    published_contents = F.and_(
        F.eq("metadata.category", "AI"),
        F.eq("metadata.category", "published"),
    )

    results = await store.vector.retrieve(
        query="AI for everyone",
        filters=published_contents,
        options=QueryOptions(limit=5),
    )
    print("AND filter results:")
    for chunk in results:
        print(f"  - {chunk.content}")

    # Nested logic (AND + OR + NOT)
    tech_or_research = F.and_(
        F.or_(
            F.eq("metadata.topic", "AI"),
            F.eq("metadata.topic", "food"),
        ),
        F.not_(F.eq("metadata.category", "published")),
    )

    await store.fulltext.delete(filters=tech_or_research)
    print("Deleted entries matching nested logic")

    await em_invoker.release_resources()


if __name__ == "__main__":
    asyncio.run(main())
