import asyncio

from gllm_evals.evaluator.classical_retrieval_evaluator import (
    ClassicalRetrievalEvaluator,
)
from gllm_evals.types import RetrievalData


async def main() -> None:
    """Run a classical retrieval evaluation example."""
    data = RetrievalData(
        retrieved_chunks={
            "chunk1": 9.0,
            "chunk2": 0.0,
            "chunk3": 0.3,
            "chunk4": 0.1,
            "chunk5": 0.2,
            "chunk6": 0.4,
            "chunk7": 0.5,
            "chunk8": 0.6,
            "chunk9": 0.7,
            "chunk10": 0.8,
        },
        ground_truth_chunk_ids=["chunk9", "chunk3", "chunk2"],
    )

    evaluator = ClassicalRetrievalEvaluator(k=[5, 10])
    result = await evaluator.evaluate(data)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
