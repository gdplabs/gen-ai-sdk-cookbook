import asyncio

from gllm_evals.metrics.retrieval.pytrec_metric import PyTrecMetric, PyTrecEvalMetric
from gllm_evals.types import RetrievalData


async def main() -> None:
    """Run a simple PyTrec evaluation example (MAP, NDCG, Precision, Recall)."""

    # RetrievalData schema for non-LLM ground-truth-based evaluation
    data = RetrievalData(
        retrieved_chunks={
            "chunk_12": 0.95,  # Highly ranked chunk
            "chunk_45": 0.88,
            "chunk_78": 0.72,
            "chunk_05": 0.65,
        },
        ground_truth_chunk_ids=[
            "chunk_12",
            "chunk_78",
            "chunk_99",
        ],  # Actual target chunks
    )

    # Initialize the metric computing specific metrics at k=3
    metric = PyTrecMetric(
        metrics=[
            PyTrecEvalMetric.NDCG,
            PyTrecEvalMetric.PRECISION,
            PyTrecEvalMetric.RECALL,
        ],
        k=3,
    )

    result = await metric.evaluate(data)

    print("Information Retrieval Metrics @ 3:")
    for key, val in result["pytrec"].items():
        print(f"- {key}: {val['score']}")


if __name__ == "__main__":
    asyncio.run(main())
