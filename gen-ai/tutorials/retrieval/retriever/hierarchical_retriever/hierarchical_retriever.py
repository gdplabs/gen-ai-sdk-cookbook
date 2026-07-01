"""Example of using HierarchicalRetriever for progressive multi-level document retrieval.

References:
    [1] https://gdplabs.gitbook.io/sdk/tutorials/retrieval/retriever/hierarchical-retriever
"""

import asyncio

from gllm_retrieval.retriever import VectorRetriever
from gllm_retrieval.retriever.hierarchical_retriever import (
    HierarchicalRetriever,
    HierarchicalRetrieverConfig,
    LevelConfig,
    ConstraintMode
)


async def main() -> None:
    document_retriever = VectorRetriever(data_store=document_store)
    chunk_retriever = VectorRetriever(data_store=chunk_store)

    config = HierarchicalRetrieverConfig(
        levels=[
            LevelConfig(
                name="document",
                retriever=document_retriever,
                top_k=5,
                filter_key="document_id",
                constrain_by=None
            ),
            LevelConfig(
                name="chunk",
                retriever=chunk_retriever,
                top_k=10,
                filter_key="document_id",
                constrain_by=ConstraintMode.PREVIOUS
            )
        ],
        output_level="chunk"
    )

    retriever = HierarchicalRetriever(config=config)

    results = await retriever.retrieve("What is machine learning?")


if __name__ == "__main__":
    asyncio.run(main())
