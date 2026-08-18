"""
Field-targeted BM25 search using QueryOptions.search_fields.

Demonstrates the split between `search_fields` (which fields BM25 matches/boosts)
and `include_fields` (which fields are returned in the result payload, i.e.
_source projection).

`search_fields` is BM25-only and is supported on Elasticsearch/OpenSearch
full-text retrieval. It is NOT supported by InMemoryDataStore or ChromaDataStore
(the backends the other scripts in this folder use), so this example requires a
running Elasticsearch or OpenSearch instance.

Reference:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/data-store/query-filter#field-targeted-search-bm25
"""

import asyncio
import os

from dotenv import load_dotenv
from gllm_core.schema import Chunk
from gllm_datastore.core.filters import QueryOptions, filter as F
from gllm_datastore.data_store.elasticsearch.data_store import ElasticsearchDataStore

load_dotenv()


async def main() -> None:
    """Show default BM25, boosted search_fields, and the search-vs-projection split."""
    # Runs against a real Elasticsearch/OpenSearch cluster. Point it at your
    # instance via the ELASTICSEARCH_URL env var (or .env); defaults to local.
    es_url = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")

    store = (
        ElasticsearchDataStore(
            index_name="query-filter-bm25",
            url=es_url,
            request_timeout=30,
        )
        .with_fulltext(query_field="text")
    )

    chunks = [
        Chunk(
            id="doc:1",
            content="Our refund policy covers returns within 30 days.",
            metadata={
                "source": "gl-sdk-docs",
                "title": "Refunds",
                "summary": "Returns policy overview.",
            },
        ),
        Chunk(
            id="doc:2",
            content="Shipping times vary by region.",
            metadata={
                "source": "internal-blog",
                "title": "Logistics",
                "summary": "Delivery information.",
            },
        ),
    ]
    await store.fulltext.create(chunks)

    # (a) Default BM25: no search_fields -> searches only the configured query
    #     field ("text"). Identical to the behavior before this option existed.
    default_results = await store.fulltext.retrieve(
        strategy="bm25",
        query="refund policy",
        options=QueryOptions(limit=10),
    )
    print("Default BM25 (searches the configured query field only):")
    for chunk in default_results:
        print(f"  - {chunk.content}")

    # (b) BM25 with search_fields: search/boost specific fields. The ^N suffix
    #     is the Elasticsearch/OpenSearch boost weight. Here metadata.source is
    #     boosted x3 so matches there rank higher than matches in `text`.
    boosted_results = await store.fulltext.retrieve(
        strategy="bm25",
        query="refund policy",
        options=QueryOptions(
            search_fields=["text", "metadata.source^3"],
            limit=10,
        ),
    )
    print("\nBM25 with search_fields (boosted metadata.source^3):")
    for chunk in boosted_results:
        print(f"  - {chunk.content}")

    # (c) search_fields vs include_fields split: BM25 searches the boosted
    #     fields while the result payload only returns the projected fields.
    split_results = await store.fulltext.retrieve(
        strategy="bm25",
        query="refund policy",
        filters=F.eq("metadata.source", "gl-sdk-docs"),
        options=QueryOptions(
            search_fields=["text", "metadata.source^3"],
            include_fields=["text", "metadata.summary"],
            limit=10,
        ),
    )
    print(
        "\nBM25 search_fields combined with a different include_fields (projection):"
    )
    for chunk in split_results:
        print(f"  - {chunk.content} (summary={chunk.metadata.get('summary')})")


if __name__ == "__main__":
    asyncio.run(main())
