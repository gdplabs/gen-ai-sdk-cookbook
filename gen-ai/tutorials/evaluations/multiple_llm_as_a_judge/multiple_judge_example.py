"""
Multiple LLM-as-a-Judge Example

This tutorial demonstrates the Multiple LLM-as-a-Judge approach, an advanced
evaluation method that uses multiple language models as judges to evaluate
tasks in parallel and aggregate their results using ensemble methods.

Benefits:
1. **Higher Alignment**: Multiple judges provide more reliable evaluations
2. **Faster Human Annotation**: Humans only need to review cases with <100% agreement
3. **Human Alignment**: 100% agreement score indicates high alignment with human judgment

Features:
- Supports both categorical and numeric evaluations
- Flexible ensemble methods (median, average rounded)
- Agreement score calculation
- Judge variance calculation
"""

import asyncio
import os
from dotenv import load_dotenv

from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.judge.multiple_llm_as_judge import MultipleLLMAsJudge
from gllm_evals import load_simple_qa_dataset

load_dotenv()


# ============================================================================
# Basic Multiple LLM-as-a-Judge Example
# ============================================================================


async def example_basic_multiple_judges() -> None:
    """Example: Using multiple LLM judges with the evaluate function."""
    # Define multiple judge models
    judge_models = [
        {
            "provider_model_id": "openai/gpt-4o",
            "model_credentials": os.getenv("OPENAI_API_KEY"),
        },
        {
            "provider_model_id": "openai/gpt-4.1",
            "model_credentials": os.getenv("OPENAI_API_KEY"),
        },
    ]

    # Load dataset
    data = load_simple_qa_dataset('./dataset_examples')

    # Create evaluator with multiple judges
    evaluator = GEvalGenerationEvaluator(
        judge=MultipleLLMAsJudge(judge_models=judge_models),
        model_credentials=os.getenv("GOOGLE_API_KEY"),
    )

    # Evaluate the first data point
    result = await evaluator.evaluate(data.dataset[0])
    print("Multiple LLM-as-a-Judge Result:")
    print(result)
    print()


async def main() -> None:
    """Run all examples."""
    await example_basic_multiple_judges()


if __name__ == "__main__":
    asyncio.run(main())
