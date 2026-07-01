"""Example of using FulltextRetriever for full-text search with BM25 and filter support.

References:
    [1] https://gdplabs.gitbook.io/sdk/tutorials/retrieval/retriever/fulltext-retriever
"""

import asyncio

from gllm_datastore.core.filters import filter as F
from gllm_datastore.data_store.elasticsearch.fulltext import SupportedQueryMethods
from gllm_retrieval.retriever import FulltextRetriever


async def main() -> None:
    # data_store = ElasticsearchDataStore(...).with_fulltext(index_name="my_index")
    retriever = FulltextRetriever(data_store=data_store)

    results = await retriever.retrieve(
        query_filter=F.eq("metadata.category", "AI"),
        top_k=10
    )

    results = await retriever.retrieve(
        "search query",
        top_k=10,
        strategy=SupportedQueryMethods.BM25,
        k1=1.5,
        b=0.75
    )

    batch_results = await retriever.retrieve(
        ["query 1", "query 2"],
        top_k=10,
        strategy="bm25"
    )


if __name__ == "__main__":
    asyncio.run(main())
