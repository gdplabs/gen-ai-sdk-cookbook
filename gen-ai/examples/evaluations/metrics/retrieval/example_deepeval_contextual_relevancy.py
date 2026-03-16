import asyncio
import json
import os

from gllm_evals.dataset import load_simple_rag_dataset
from gllm_evals.metrics.retrieval.deepeval_contextual_relevancy import (
    DeepEvalContextualRelevancyMetric,
)
from gllm_evals.types import RAGData
from dotenv import load_dotenv

load_dotenv()


async def main():
    """Main function."""
    data = load_simple_rag_dataset()
    data = data.load()
    data = RAGData(
        query=data[0]["query"],
        generated_response=data[0]["generated_response"],
        retrieved_context=data[0]["retrieved_context"],
    )

    # Configure the tool correctness metric
    metric = DeepEvalContextualRelevancyMetric(
        model_credentials=os.getenv("GOOGLE_API_KEY"),
    )
    result = await metric.evaluate(data)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
