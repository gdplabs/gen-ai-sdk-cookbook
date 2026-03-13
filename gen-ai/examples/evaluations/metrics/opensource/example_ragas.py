import asyncio
import os

from ragas.metrics import LLMContextPrecisionWithoutReference

from gllm_evals.constant import DefaultValues
from gllm_evals.metrics.opensource.ragas import RAGASMetric
from gllm_evals.types import RAGData
from gllm_evals.utils.ragas_wrapper import RagasLLMWrapper
from gllm_inference.builder.build_lm_invoker import build_lm_invoker


async def main() -> None:
    """Run a simple RAGAS wrapper evaluation example."""

    # 1. First, we need an LM Wrapper compatible with RAGAS
    invoker = build_lm_invoker(model=DefaultValues.MODEL, credentials=os.getenv("OPENAI_API_KEY"))
    ragas_model = RagasLLMWrapper(lm_invoker=invoker)

    # 2. Instantiate the Base RAGAS Metric (e.g. LLMContextPrecisionWithoutReference)
    base_ragas_metric = LLMContextPrecisionWithoutReference(llm=ragas_model)

    # 3. Wrap it using our framework's RAGASMetric
    metric = RAGASMetric(metric=base_ragas_metric, name="My RAGAS Precision")

    # 4. Define the evaluation data
    # RAGASMetric typically requires query, generated_response, requested_context
    dataset = [
        RAGData(
            query="What is the capital of France?",
            generated_response="Paris is the capital of France.",
            retrieved_context=[
                "Paris is the capital and most populous city of France.",
                "It is located along the Seine River in the north-central part of the country.",
            ],
        )
    ]

    for data in dataset:
        result = await metric.evaluate(data)
        print("Dataset Query:", data["query"])
        # Result uses metric name
        print("Result:", result.get("My RAGAS Precision", result))
        print()


if __name__ == "__main__":
    asyncio.run(main())
