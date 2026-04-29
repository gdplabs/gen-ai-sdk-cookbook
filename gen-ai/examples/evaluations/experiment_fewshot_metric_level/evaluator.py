"""Evaluator module for running few-shot experiments with metric-level few-shot support."""

import asyncio
import os
from pathlib import Path
from typing import Literal

import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(Path(__file__).parent / ".env")

import sys

from gllm_evals.metrics.generation import (
    GEvalCompletenessMetric,
    GEvalGroundednessMetric,
    GEvalRedundancyMetric,
)
from gllm_evals.types import LLMTestData
from experiment_fewshot_metric_level.utils import convert_structured_fewshot_to_string


async def evaluate_row(
    row: pd.Series,
    fewshot_data: dict,
    eval_model: str,
    fewshot_mode: Literal["append", "replace"] = "replace",
) -> dict:
    """Evaluate a single row with metric-level few-shot examples.

    Args:
        row (pd.Series): Row to evaluate.
        fewshot_data (dict): Few-shot examples data.
        eval_model (str): Model for evaluation.
        fewshot_mode (Literal["append", "replace"], optional): Few-shot mode. Defaults to "replace".

    Returns:
        dict: Evaluation results.
    """
    question_id = str(int(row["question_id"]))

    if question_id not in fewshot_data:
        raise ValueError(f"Question ID {question_id} not found in few-shot data")

    fewshot_examples = fewshot_data[question_id]

    # Convert structured format to string for each metric
    completeness_fewshot = fewshot_examples.get("fewshot_completeness", [])
    if isinstance(completeness_fewshot, list):
        completeness_fewshot = convert_structured_fewshot_to_string(completeness_fewshot)

    redundancy_fewshot = fewshot_examples.get("fewshot_redundancy", [])
    if isinstance(redundancy_fewshot, list):
        redundancy_fewshot = convert_structured_fewshot_to_string(redundancy_fewshot)

    groundedness_fewshot = fewshot_examples.get("fewshot_groundedness", [])
    if isinstance(groundedness_fewshot, list):
        groundedness_fewshot = convert_structured_fewshot_to_string(groundedness_fewshot)

    # Handle retrieval_context - ensure it's NEVER None or empty
    context = row.get("retrieved_context")
    
    # Comprehensive None/NaN handling
    if context is None or pd.isna(context) or str(context).strip() == "":
        # Fallback to context column if available
        context = row.get("context")
        if context is None or pd.isna(context) or str(context).strip() == "":
            context = "No context available"
    
    # Ensure it's a string and not empty
    context_str = str(context).strip()
    if not context_str:
        context_str = "No context available"
    
    test_data = LLMTestData(
        input=str(row["question"]),
        actual_output=str(row["generated_response"]),
        expected_output=str(row["expected_response"]),
        retrieval_context=[context_str],
    )

    provider = eval_model.split("/")[0]
    key_map = {
        "google": "GOOGLE_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
        "openai": "OPENAI_API_KEY",
    }
    api_key = os.getenv(key_map.get(provider, "GOOGLE_API_KEY"))

    # Match sibling experiment pattern
    completeness_metric = GEvalCompletenessMetric(
        model=eval_model,
        model_credentials=api_key,
    )
    redundancy_metric = GEvalRedundancyMetric(
        model=eval_model,
        model_credentials=api_key,
    )
    groundedness_metric = GEvalGroundednessMetric(
        model=eval_model,
        model_credentials=api_key,
    )

    completeness_result = await completeness_metric.evaluate(
        test_data,
        temp_fewshot=completeness_fewshot,
        fewshot_mode=fewshot_mode,
    )

    redundancy_result = await redundancy_metric.evaluate(
        test_data,
        temp_fewshot=redundancy_fewshot,
        fewshot_mode=fewshot_mode,
    )

    groundedness_result = await groundedness_metric.evaluate(
        test_data,
        temp_fewshot=groundedness_fewshot,
        fewshot_mode=fewshot_mode,
    )

    # Extract scores - handle dict format with score/explanation keys
    completeness_data = completeness_result.get("completeness", {})
    if isinstance(completeness_data, dict):
        completeness_score = completeness_data.get("score", 0)
        completeness_reason = completeness_data.get("explanation", "")
    else:
        completeness_score = completeness_data
        completeness_reason = ""

    redundancy_data = redundancy_result.get("redundancy", {})
    if isinstance(redundancy_data, dict):
        redundancy_score = redundancy_data.get("score", 0)
        redundancy_reason = redundancy_data.get("explanation", "")
    else:
        redundancy_score = redundancy_data
        redundancy_reason = ""

    groundedness_data = groundedness_result.get("groundedness", {})
    if isinstance(groundedness_data, dict):
        groundedness_score = groundedness_data.get("score", 0)
        groundedness_reason = groundedness_data.get("explanation", "")
    else:
        groundedness_score = groundedness_data
        groundedness_reason = ""

    autoeval_rr = calculate_relevance_rating(
        completeness_score,
        redundancy_score,
        groundedness_score,
    )

    return {
        "question_id": row["question_id"],
        "question": row["question"],
        "generated_response": row["generated_response"],
        "retrieved_context": row["retrieved_context"],
        "expected_response": row["expected_response"],
        "predicted_completeness": completeness_score,
        "completeness_reason": completeness_reason,
        "predicted_redundancy": redundancy_score,
        "redundancy_reason": redundancy_reason,
        "predicted_groundedness": groundedness_score,
        "groundedness_reason": groundedness_reason,
        "autoeval_rr": autoeval_rr,
    }


def calculate_relevance_rating(completeness: int, redundancy: int, groundedness: int) -> str:
    """Calculate overall relevance rating from metric scores.

    Args:
        completeness (int): Completeness score (1-3).
        redundancy (int): Redundancy score (1-3).
        groundedness (int): Groundedness score (1-3).

    Returns:
        str: Relevance rating (Good/Acceptable/Bad).
    """
    if completeness == 3 and redundancy == 1 and groundedness == 3:
        return "Good"
    elif completeness >= 2 and redundancy <= 2 and groundedness >= 2:
        return "Acceptable"
    else:
        return "Bad"


async def evaluate_dataframe(
    df: pd.DataFrame,
    fewshot_data: dict,
    eval_model: str,
    num_workers: int = 5,
    fewshot_mode: Literal["append", "replace"] = "replace",
) -> pd.DataFrame:
    """Evaluate all rows in dataframe with parallel processing.

    Args:
        df (pd.DataFrame): Dataframe to evaluate.
        fewshot_data (dict): Few-shot examples data.
        eval_model (str): Model for evaluation.
        num_workers (int, optional): Number of parallel workers. Defaults to 5.
        fewshot_mode (Literal["append", "replace"], optional): Few-shot mode. Defaults to "replace".

    Returns:
        pd.DataFrame: Evaluation results.
    """
    print(f"\n🚀 Starting evaluation with {num_workers} workers for {len(df)} rows...")
    print(f"   Using metric.evaluate() with temp_fewshot (mode: {fewshot_mode})")

    semaphore = asyncio.Semaphore(num_workers)

    async def evaluate_with_semaphore(row_tuple: tuple) -> dict:
        async with semaphore:
            idx, row = row_tuple
            try:
                result = await evaluate_row(row, fewshot_data, eval_model, fewshot_mode)
                print(f"   ✓ Processed row {idx + 1}/{len(df)} (Q{row['question_id']}, index: {idx})")
                return result
            except Exception as e:
                print(f"   ✗ Error processing row {idx + 1} (Q{row['question_id']}): {e}")
                raise

    tasks = [evaluate_with_semaphore(row_tuple) for row_tuple in df.iterrows()]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    errors = [r for r in results if isinstance(r, Exception)]
    if errors:
        for err in errors:
            print(f"   ✗ Task failed: {err}")
        raise errors[0]

    print(f"\n✅ Completed processing all {len(df)} rows!")

    return pd.DataFrame(results)


async def run_experiment(
    df: pd.DataFrame,
    fewshot_data: dict,
    eval_model: str,
    num_workers: int = 5,
    fewshot_mode: Literal["append", "replace"] = "replace",
) -> pd.DataFrame:
    """Run complete experiment evaluation.

    Args:
        df (pd.DataFrame): Experiment dataframe.
        fewshot_data (dict): Few-shot examples data.
        eval_model (str): Model for evaluation.
        num_workers (int, optional): Number of parallel workers. Defaults to 5.
        fewshot_mode (Literal["append", "replace"], optional): Few-shot mode. Defaults to "replace".

    Returns:
        pd.DataFrame: Evaluation results.
    """
    return await evaluate_dataframe(df, fewshot_data, eval_model, num_workers, fewshot_mode)
