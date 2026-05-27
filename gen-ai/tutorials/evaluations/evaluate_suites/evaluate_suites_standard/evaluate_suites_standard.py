"""Example script to evaluate multiple data partitions using evaluate_suites.

This example demonstrates the basic usage of evaluate_suites() with:
- Inline data (LLMTestCase list) per suite
- Different evaluator types per suite (GEvalGenerationEvaluator, CompositeEvaluator)
- Shared experiment tracker and run_id
- Per-suite namespaced dataset names

Authors:
Kalvin (kalvinsupriadi3@gmail.com)
"""

import asyncio
import json
import os

from dotenv import load_dotenv
from gllm_evals import EvalSuite, LLMTestCase, evaluate_suites
from gllm_evals.evaluator.composite_evaluator import CompositeEvaluator
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.metrics.generation.geval_groundedness import GEvalGroundednessMetric
from gllm_inference.lm_invoker import build_lm_invoker

load_dotenv()


async def main() -> None:
    """Run evaluate_suites with different evaluators for different data suites."""
    judge_model = build_lm_invoker(
        model_id="openai/gpt-5-nano",
        credentials=os.getenv("OPENAI_API_KEY"),
    )

    # Suite 1: General knowledge questions with generation evaluator
    qa_suite = EvalSuite(
        name="qa",
        data=[
            LLMTestCase(
                input="What is the capital of France?",
                actual_output="Paris is the capital of France.",
                expected_output="Paris",
                retrieved_context="France is a country in Europe. Paris is the largest city.",
            ),
            LLMTestCase(
                input="What is the largest planet in our solar system?",
                actual_output="Jupiter is the largest planet.",
                expected_output="Jupiter",
                retrieved_context="Jupiter is the fifth planet from the Sun.",
            ),
        ],
        evaluators=[GEvalGenerationEvaluator(models=[judge_model])],
    )

    # Suite 2: Retrieved context evaluation with groundedness evaluator
    rag_suite = EvalSuite(
        name="rag",
        data=[
            LLMTestCase(
                input="What year was the Eiffel Tower built?",
                actual_output="The Eiffel Tower was built in 1889.",
                expected_output="1889",
                retrieved_context="The Eiffel Tower, built for the 1889 World's Fair in Paris, is an iconic iron lattice tower.",  # noqa: E501
            ),
            LLMTestCase(
                input="Who wrote Romeo and Juliet?",
                actual_output="William Shakespeare wrote Romeo and Juliet.",
                expected_output="William Shakespeare",
                retrieved_context="Romeo and Juliet is a tragedy written by William Shakespeare early in his career.",
            ),
        ],
        evaluators=[
            CompositeEvaluator(
                metrics=[GEvalGroundednessMetric(models=[judge_model])],
                name="groundedness",
            )
        ],
    )

    # Suite 3: Auto-generated suite name with generation evaluator
    auto_named_suite = EvalSuite(
        data=[
            LLMTestCase(
                input="What is 2 + 2?",
                actual_output="2 + 2 equals 4.",
                expected_output="4",
            ),
        ],
        evaluators=[GEvalGenerationEvaluator(models=[judge_model])],
    )

    result = await evaluate_suites(
        suites=[qa_suite, rag_suite, auto_named_suite],
        dataset_name="multi_suite_evaluation",
    )

    print(json.dumps(result.model_dump(), indent=2))


if __name__ == "__main__":
    asyncio.run(main())
