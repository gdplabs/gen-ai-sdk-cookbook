"""Evaluate Helper Function Example - Standard Dataset.

This tutorial demonstrates how to use the `evaluate()` convenience helper function
with standard datasets (local files or built-in datasets).

The evaluate() function supports:
- Structured evaluation rules (each record receives the same evaluation treatment)
- Multiple data sources (HuggingFace, Langfuse, local files)
- Custom inference functions
- Multiple evaluators
- Experiment tracking
- Summary evaluators for aggregate metrics
"""

import asyncio
import os

from dotenv import load_dotenv

from gllm_evals import load_simple_qa_dataset
from gllm_evals.evaluate import evaluate
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.utils.shared_functionality import inference_fn

load_dotenv()


async def main() -> None:
    """Run evaluation with the built-in simple QA dataset.

    This example demonstrates the basic usage of evaluate() with:
    - Built-in dataset loader
    - Default inference function
    - Single evaluator
    """
    results = await evaluate(
        data=load_simple_qa_dataset('./dataset_examples'),
        inference_fn=inference_fn,
        evaluators=[
            GEvalGenerationEvaluator(
                model_credentials=os.getenv("GOOGLE_API_KEY")
            )
        ],
    )
    print(results)


if __name__ == "__main__":
    # Run the basic example
    asyncio.run(main())
