"""Utility functions for few-shot experiments."""

import json
from pathlib import Path
from typing import Any

import pandas as pd


def convert_structured_fewshot_to_string(structured_examples: list[dict]) -> str:
    """Convert structured few-shot examples to string format for temp_fewshot.

    Args:
        structured_examples (list[dict]): List of structured examples.

    Returns:
        str: Formatted few-shot string.
    """
    if not structured_examples:
        return ""

    examples = []
    for idx, example in enumerate(structured_examples, 1):
        parts = [f"Example {idx}:"]

        if "explanation" in example:
            parts.append(f"Explanation: {example['explanation']}")

        if "question" in example:
            parts.append(f"Question: {example['question']}")

        if "expected_response" in example:
            parts.append(f"Expected Output: {example['expected_response']}")

        if "generated_response" in example:
            parts.append(f"Generated Output: {example['generated_response']}")

        if "score" in example:
            parts.append(f"Score: {example['score']}.")

        examples.append("\n".join(parts))

    return "FEW-SHOT EXAMPLES \n" + "\n\n".join(examples)


def load_fewshot_data(json_path: Path | str) -> dict:
    """Load few-shot examples from JSON file.

    Args:
        json_path (Path | str): Path to few-shot JSON file.

    Returns:
        dict: Few-shot examples data.

    Raises:
        FileNotFoundError: If JSON file not found.
        json.JSONDecodeError: If JSON is invalid.
    """
    json_path = Path(json_path)

    if not json_path.exists():
        raise FileNotFoundError(f"Few-shot JSON not found: {json_path}")

    with open(json_path, encoding="utf-8") as f:
        return json.load(f)


def load_experiment_data(csv_path: Path | str) -> pd.DataFrame:
    """Load experiment data from CSV file.

    Args:
        csv_path (Path | str): Path to experiment CSV file.

    Returns:
        pd.DataFrame: Experiment data.

    Raises:
        FileNotFoundError: If CSV file not found.
    """
    csv_path = Path(csv_path)

    if not csv_path.exists():
        raise FileNotFoundError(f"Experiment CSV not found: {csv_path}")

    return pd.read_csv(csv_path)


def add_retrieved_context(df: pd.DataFrame, fewshot_data: dict) -> pd.DataFrame:
    """Add retrieved_context column from few-shot data or CSV context column.

    Args:
        df (pd.DataFrame): Experiment dataframe.
        fewshot_data (dict): Few-shot examples data.

    Returns:
        pd.DataFrame: Dataframe with retrieved_context column.

    Raises:
        ValueError: If question_id not found in few-shot data.
    """
    if "retrieved_context" in df.columns:
        df["retrieved_context"] = df["retrieved_context"].fillna("No context available")
        return df

    # If CSV has 'context' column, rename it to 'retrieved_context'
    if "context" in df.columns:
        df["retrieved_context"] = df["context"].fillna("No context available")
        return df

    def get_retrieved_context(question_id: int) -> str:
        question_id_str = str(int(question_id))

        if question_id_str not in fewshot_data:
            raise ValueError(f"Question ID '{question_id_str}' not found in few-shot data")

        context = fewshot_data[question_id_str].get("retrieved_context", "")

        if not context:
            raise ValueError(f"Question ID '{question_id_str}' has no 'retrieved_context'")

        return context

    df["retrieved_context"] = df["question_id"].apply(get_retrieved_context)
    return df


def filter_by_question_ids(df: pd.DataFrame, question_ids: list[int] | None) -> pd.DataFrame:
    """Filter dataframe by question IDs.

    Args:
        df (pd.DataFrame): Experiment dataframe.
        question_ids (list[int] | None): Question IDs to filter. None for all.

    Returns:
        pd.DataFrame: Filtered dataframe.
    """
    if question_ids is None:
        return df

    question_ids_str = set(str(qid) for qid in question_ids)
    return df[df["question_id"].astype(str).isin(question_ids_str)]


def filter_by_fewshot_availability(df: pd.DataFrame, fewshot_data: dict) -> pd.DataFrame:
    """Filter dataframe to only include questions with few-shot examples.

    Args:
        df (pd.DataFrame): Experiment dataframe.
        fewshot_data (dict): Few-shot examples data.

    Returns:
        pd.DataFrame: Filtered dataframe.
    """
    fewshot_question_ids = set(fewshot_data.keys())
    return df[df["question_id"].astype(str).isin(fewshot_question_ids)]


def remove_existing_predictions(df: pd.DataFrame) -> pd.DataFrame:
    """Remove existing prediction columns from dataframe.

    Args:
        df (pd.DataFrame): Experiment dataframe.

    Returns:
        pd.DataFrame: Dataframe without prediction columns.
    """
    columns_to_remove = [
        "is_relevant",
        "completeness",
        "completeness_reason",
        "redundancy",
        "redundancy_reason",
        "groundedness",
        "groundedness_reason",
        "autoeval_rr",
    ]

    existing_columns = [col for col in columns_to_remove if col in df.columns]

    if existing_columns:
        df = df.drop(columns=existing_columns)

    return df


def save_results(
    df: pd.DataFrame,
    output_dir: Path | str,
    experiment_name: str,
    question_ids: list[int] | None = None,
) -> Path:
    """Save evaluation results to CSV file.

    Args:
        df (pd.DataFrame): Results dataframe.
        output_dir (Path | str): Output directory.
        experiment_name (str): Experiment name.
        question_ids (list[int] | None, optional): Question IDs evaluated. Defaults to None.

    Returns:
        Path: Path to saved CSV file.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{experiment_name}_fewshot_metric_level"

    if question_ids is not None:
        qid_suffix = "_".join(str(qid) for qid in sorted(question_ids)[:5])
        if len(question_ids) > 5:
            qid_suffix += f"_plus{len(question_ids) - 5}more"
        filename += f"_qids_{qid_suffix}"

    filename += ".csv"

    output_path = output_dir / filename
    df.to_csv(output_path, index=False)

    return output_path


def save_summary(
    summary: dict,
    output_dir: Path | str,
    experiment_name: str,
) -> Path:
    """Save experiment summary to JSON file.

    Args:
        summary (dict): Summary data.
        output_dir (Path | str): Output directory.
        experiment_name (str): Experiment name.

    Returns:
        Path: Path to saved JSON file.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"{experiment_name}_summary.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    return output_path


def print_experiment_info(
    experiment_config: dict,
    eval_model: str,
    num_workers: int,
    total_rows: int,
    question_ids: list[int] | None,
    fewshot_mode: str,
) -> None:
    """Print experiment information.

    Args:
        experiment_config (dict): Experiment configuration.
        eval_model (str): Evaluation model.
        num_workers (int): Number of workers.
        total_rows (int): Total rows to evaluate.
        question_ids (list[int] | None): Question IDs to evaluate.
        fewshot_mode (str): Few-shot mode (append/replace).
    """
    print("=" * 80)
    print("EXPERIMENT CONFIGURATION")
    print("=" * 80)
    print(f"Experiment Index: {experiment_config['index']}")
    print(f"Model Provider: {experiment_config.get('model_provider', 'N/A')}")
    model_id = experiment_config.get('model_id') or experiment_config.get('provider_model_id', 'N/A')
    print(f"Model ID: {model_id}")
    print(f"Evaluation Model: {eval_model}")
    print(f"Number of Workers: {num_workers}")
    print(f"Number of Rows: {total_rows}")
    print(f"Few-Shot Mode: {fewshot_mode}")

    if question_ids is not None:
        print(f"Question IDs: {sorted(question_ids)}")
    else:
        print("Question IDs: All")

    print("=" * 80)
    print()


def print_results_summary(
    df: pd.DataFrame,
    experiment_config: dict,
) -> None:
    """Print evaluation results summary.

    Args:
        df (pd.DataFrame): Results dataframe.
        experiment_config (dict): Experiment configuration.
    """
    print("\n" + "=" * 80)
    print("EVALUATION RESULTS SUMMARY")
    print("=" * 80)

    print(f"Experiment: {experiment_config['index']}")
    print(f"Total Rows Evaluated: {len(df)}")

    if "predicted_completeness" in df.columns:
        print(f"\nCompleteness Scores:")
        print(f"  Mean: {df['predicted_completeness'].mean():.2f}")
        print(f"  Distribution: {df['predicted_completeness'].value_counts().sort_index().to_dict()}")

    if "predicted_redundancy" in df.columns:
        print(f"\nRedundancy Scores:")
        print(f"  Mean: {df['predicted_redundancy'].mean():.2f}")
        print(f"  Distribution: {df['predicted_redundancy'].value_counts().sort_index().to_dict()}")

    if "predicted_groundedness" in df.columns:
        print(f"\nGroundedness Scores:")
        print(f"  Mean: {df['predicted_groundedness'].mean():.2f}")
        print(f"  Distribution: {df['predicted_groundedness'].value_counts().sort_index().to_dict()}")

    if "autoeval_rr" in df.columns:
        print(f"\nRelevance Rating Distribution:")
        print(f"  {df['autoeval_rr'].value_counts().to_dict()}")

    print("=" * 80)
