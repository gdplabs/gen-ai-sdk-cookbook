import asyncio
import os

from deepeval.metrics import AnswerRelevancyMetric

from gllm_evals.constant import DefaultValues
from gllm_evals.metrics.opensource.deepeval import DeepEvalMetric
from gllm_evals.types import RAGData
from gllm_evals.utils.deepeval_wrapper import DeepEvalLLMWrapper
from gllm_inference.builder.build_lm_invoker import build_lm_invoker


async def main() -> None:
    """Run a simple DeepEval wrapper evaluation example."""

    # 1. First, we need an LM Wrapper compatible with DeepEval
    # We use the built-in DeepEvalLLMWrapper around our BaseLMInvoker
    invoker = build_lm_invoker(model=DefaultValues.MODEL, credentials=os.getenv("OPENAI_API_KEY"))
    deepeval_model = DeepEvalLLMWrapper(lm_invoker=invoker)

    # 2. Instantiate the Base DeepEval Metric
    base_deepeval_metric = AnswerRelevancyMetric(threshold=0.5, model=deepeval_model)

    # 3. Wrap it using our framework's DeepEvalMetric
    metric = DeepEvalMetric(metric=base_deepeval_metric, name="My DeepEval Relevancy")

    # 4. Define the evaluation data
    # DeepEvalMetric maps to RAGData fields: query, generated_response, expected_response, retrieved_context
    dataset = [
        RAGData(  # Good case
            query="What is the capital of France?",
            generated_response="The capital of France is Paris.",
            retrieved_context=["Paris is the capital of France."],
            expected_response="",
        ),
        RAGData(  # Bad case
            query="What is the capital of France?",
            generated_response="I like eating pizza.",
            retrieved_context=["Paris is the capital of France."],
            expected_response="",
        ),
    ]

    for data in dataset:
        result = await metric.evaluate(data)
        print("Dataset Query:", data["query"])
        # DeepEvalMetric creates a namespace based on the metric's name
        print("Result:", result.get("My DeepEval Relevancy", result))
        print()


if __name__ == "__main__":
    asyncio.run(main())
