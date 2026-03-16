import asyncio
import os

from gllm_evals.constant import DefaultValues
from gllm_evals.evaluator.custom_evaluator import CustomEvaluator
from gllm_evals.metrics.generation.ragas_factual_correctness import (
    RagasFactualCorrectness,
)
from gllm_evals.metrics.retrieval.ragas_context_precision import (
    RagasContextPrecisionWithoutReference,
)
from gllm_evals.metrics.retrieval.ragas_context_recall import RagasContextRecall
from gllm_evals.types import RAGData
from dotenv import load_dotenv

load_dotenv()


async def main():
    """Main function."""
    ragas_factual_correctness = RagasFactualCorrectness(
        lm_model="openai/gpt-5-nano",
        lm_model_credentials=os.getenv("OPENAI_API_KEY"),
    )
    ragas_context_recall = RagasContextRecall(
        lm_model_credentials=os.getenv("GOOGLE_API_KEY"),
    )
    ragas_context_precision = RagasContextPrecisionWithoutReference(
        lm_model_credentials=os.getenv("GOOGLE_API_KEY"),
    )

    evaluator = CustomEvaluator(
        metrics=[
            ragas_factual_correctness,
            ragas_context_recall,
            ragas_context_precision,
        ],
        name="my_evaluator",
    )

    data = RAGData(
        query="When was the first super bowl?",
        generated_response="The first superbowl was held on Jan 15, 1967",
        retrieved_context=[
            "The First AFL-NFL World Championship Game was an American football game played on January 15, 1967, "
            "at the Los Angeles Memorial Coliseum in Los Angeles."
        ],
        expected_response="The first superbowl was held on Jan 15, 1967",
    )
    result = await evaluator.evaluate(data)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
