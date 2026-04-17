"""
Getting Started with GenAI Evaluator SDK

This tutorial demonstrates how to:
1. Install the GenAI Evaluator SDK
2. Set up your API credentials
3. Run your first evaluation using GEvalGenerationEvaluator

The evaluator evaluates RAG pipeline output using multiple metrics:
- Completeness: Measures if the output covers all required information
- Groundedness: Checks if the output is supported by the retrieved context
- Redundancy: Identifies unnecessary repetition
- Language Consistency: Ensures the output language matches the input
- Refusal Alignment: Validates if refusal behavior is appropriate
"""

import asyncio
import os
from dotenv import load_dotenv

from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.types import RAGData

load_dotenv()


async def main() -> None:
    """Run a simple evaluation example."""
    # Initialize the evaluator with your model credentials
    # By default, GEvalGenerationEvaluator uses Gemini 3 Pro from Google
    evaluator = GEvalGenerationEvaluator(
        model_credentials=os.getenv("GOOGLE_API_KEY")
    )

    # Define your test data
    data = RAGData(
        query="What is the capital of France?",
        expected_response="Paris",
        generated_response="New York",
        retrieved_context="Paris is the capital of France.",
    )

    # Run the evaluation
    result = await evaluator.evaluate(data)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
