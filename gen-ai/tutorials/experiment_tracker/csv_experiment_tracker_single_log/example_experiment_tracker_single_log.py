"""Example of using the CSVExperimentTracker with a single manual log.

Authors:
    Apri Dwi Rachmadi (apri.d.rachmadi@gdplabs.id)

References:
    NONE
"""

import asyncio

from gllm_evals.experiment_tracker import CSVExperimentTracker
from gllm_evals.types import LLMTestCase

tracker = CSVExperimentTracker(
    "my_project", output_dir="./my_experiments", score_key="score"
)

evaluator_results = {
    "generation": {
        "aggregate_explanation": "The following metrics failed to meet expectations:\n1. Completeness is 0 (should be >= 1)\n2. Groundedness is 0 (should be >= 1)",
        "aggregate_success": False,
        "aggregate_score": 0.3333333333333333,
        "completeness": {
            "score": 0.0,
            "explanation": "The minimum key facts are: [A] Paris. The generated response provides 'New York' as the answer, which directly contradicts the correct information.",
            "rubric_score": 1,
            "success": False,
            "threshold": 1.0,
            "strict_mode": False,
            "higher_is_better": True,
            "model_id": "google/gemini-3-flash-preview",
        },
        "redundancy": {
            "score": 0.0,
            "explanation": "The response is extremely concise and provides the name of the city exactly once.",
            "rubric_score": 1,
            "success": True,
            "threshold": 0.5,
            "strict_mode": False,
            "higher_is_better": False,
            "model_id": "google/gemini-3-flash-preview",
        },
        "groundedness": {
            "score": 0.0,
            "explanation": "The response identifies New York as the capital of France, which is a critical factual error.",
            "rubric_score": 1,
            "success": False,
            "threshold": 1.0,
            "strict_mode": False,
            "higher_is_better": True,
            "model_id": "google/gemini-3-flash-preview",
        },
        "is_refusal": False,
    }
}

data = LLMTestCase(
    input="What is the capital of France?",
    expected_output="Paris",
    actual_output="New York",
    retrieved_context="Paris is the capital of France.",
)

tracker.log(
    evaluation_result=evaluator_results,
    dataset_name="sample_qa_dataset",
    data=data,
)
