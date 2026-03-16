import asyncio
import json
import os

from gllm_evals.constant import DefaultValues
from gllm_evals.evaluator.custom_evaluator import CustomEvaluator
from gllm_evals.metrics.generation.langchain_conciseness import (
    LangChainConcisenessMetric,
)
from gllm_evals.metrics.generation.langchain_correctness import (
    LangChainCorrectnessMetric,
)
from gllm_evals.metrics.generation.langchain_groundedness import (
    LangChainGroundednessMetric,
)
from gllm_evals.metrics.generation.langchain_hallucination import (
    LangChainHallucinationMetric,
)
from gllm_evals.metrics.generation.langchain_helpfulness import (
    LangChainHelpfulnessMetric,
)
from gllm_evals.types import RAGData
from dotenv import load_dotenv
from gllm_evals.dataset import load_simple_rag_dataset

load_dotenv()


async def main():
    """Example of using LangChainOpenEvals to evaluate a RAG app."""
    metrics = [
        LangChainConcisenessMetric(
            model=DefaultValues.MODEL,
            model_credentials=os.getenv("GOOGLE_API_KEY"),
        ),
        LangChainCorrectnessMetric(
            model=DefaultValues.MODEL,
            model_credentials=os.getenv("GOOGLE_API_KEY"),
        ),
        LangChainHallucinationMetric(
            model=DefaultValues.MODEL,
            model_credentials=os.getenv("GOOGLE_API_KEY"),
        ),
        LangChainHelpfulnessMetric(
            model=DefaultValues.MODEL,
            model_credentials=os.getenv("GOOGLE_API_KEY"),
        ),
        LangChainGroundednessMetric(
            model=DefaultValues.MODEL,
            model_credentials=os.getenv("GOOGLE_API_KEY"),
        ),
    ]

    data = load_simple_rag_dataset()
    data = data.load()

    data = RAGData(
        query=data[0]["query"],
        expected_response=data[0]["expected_response"],
        generated_response=data[0]["generated_response"],
        retrieved_context=data[0]["retrieved_context"],
    )

    evaluator = CustomEvaluator(metrics, name="langchain_openeval")

    result = await evaluator.evaluate(data)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
