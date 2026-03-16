import asyncio
import json
import os
from pathlib import Path

from gllm_evals.dataset import load_simple_rag_dataset
from gllm_evals.metrics.retrieval.geval_context_sufficiency import (
    GEvalContextSufficiencyMetric,
)
from gllm_evals.types import RAGData
from dotenv import load_dotenv

load_dotenv()


async def main():
    """Main function."""
    data_dir = Path(__file__).resolve().parent / "dataset_examples"
    data = load_simple_rag_dataset(data_dir)
    data = data.load()
    data = RAGData(
        query=data[0]["query"],
        retrieved_context=data[0]["retrieved_context"],
    )

    # Configure the tool correctness metric
    metric = GEvalContextSufficiencyMetric(
        model_credentials=os.getenv("GOOGLE_API_KEY"),
    )
    result = await metric.evaluate(data)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
