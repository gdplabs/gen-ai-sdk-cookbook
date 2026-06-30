import asyncio

from gllm_evals.metrics.retrieval.top_k_accuracy import TopKAccuracy
from gllm_evals.types import RetrievalData


async def main() -> None:
    """Run a Top-K Accuracy evaluation example."""

    # RetrievalData schema
    data = RetrievalData(
        retrieved_chunks={
            "chunk_A": 0.95,  # Rank 1
            "chunk_B": 0.88,  # Rank 2
            "chunk_C": 0.72,  # Rank 3
            "chunk_D": 0.65,  # Rank 4
            "chunk_E": 0.40,  # Rank 5
        },
        ground_truth_chunk_ids=["chunk_D"],
    )

    # Initialize the metric for k=3 and k=5
    metric = TopKAccuracy(k=[3, 5])

    result = await metric.evaluate(data)

    print("Top-K Accuracy Result:")
    top_k = getattr(result, "top_k_accuracy", result)
    for key, val in top_k.items():
        print(f"- {key}: {getattr(val, 'score', val)}")


if __name__ == "__main__":
    asyncio.run(main())
