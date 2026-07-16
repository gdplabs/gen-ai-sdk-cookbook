"""Example of using SmartSearchWebRetriever for web search with credential management.

References:
    [1] https://gdplabs.gitbook.io/sdk/tutorials/retrieval/retriever/smart-search-retriever
"""

import asyncio

from gllm_retrieval.retriever import SmartSearchWebRetriever


async def main() -> None:
    retriever = SmartSearchWebRetriever(
        base_url="https://your-smartsearch-endpoint",
        token="your-access-token"
    )

    retriever = SmartSearchWebRetriever()

    retriever = await SmartSearchWebRetriever.create(
        base_url="https://your-smartsearch-endpoint",
        token="your-access-token"
    )

    results = await retriever.retrieve(
        "What is the latest news about AI?",
        top_k=5
    )


if __name__ == "__main__":
    asyncio.run(main())
