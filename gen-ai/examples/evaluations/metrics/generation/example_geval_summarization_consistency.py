import asyncio
import json
import os

from gllm_evals.dataset import load_simple_summarization_dataset
from gllm_evals.metrics.generation.geval_summarization_consistency import (
    GEvalSummarizationConsistencyMetric,
)
from gllm_evals.types import SummaryData
from dotenv import load_dotenv

load_dotenv()


async def main():
    """Main function."""
    data = load_simple_summarization_dataset()
    data = data.load()
    data = SummaryData(
        input=data[0]["input"],
        summary=data[0]["summary"],
    )

    # Configure the tool correctness metric
    metric = GEvalSummarizationConsistencyMetric(
        model_credentials=os.getenv("GOOGLE_API_KEY"),
    )
    result = await metric.evaluate(data)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
