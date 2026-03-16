import asyncio
import json
import os
from pathlib import Path

from gllm_evals.dataset import load_simple_summarization_dataset
from gllm_evals.metrics.generation.geval_summarization_coherence import (
    GEvalSummarizationCoherenceMetric,
)
from gllm_evals.types import SummaryData
from dotenv import load_dotenv

load_dotenv()


async def main():
    """Main function."""
    data_dir = Path(__file__).resolve().parent / "dataset_examples"
    data = load_simple_summarization_dataset(data_dir)
    data = data.load()
    data = SummaryData(
        input=data[0]["input"],
        summary=data[0]["summary"],
    )

    # Configure the tool correctness metric
    metric = GEvalSummarizationCoherenceMetric(
        model_credentials=os.getenv("GOOGLE_API_KEY"),
    )
    result = await metric.evaluate(data)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
