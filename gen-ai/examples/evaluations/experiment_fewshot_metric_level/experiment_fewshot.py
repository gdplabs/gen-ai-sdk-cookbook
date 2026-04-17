"""Main script for running few-shot experiments with metric-level few-shot support.

This script runs evaluation experiments using the modern gllm-evals SDK approach
where few-shot examples are passed directly to metrics via the temp_fewshot parameter.
"""

import argparse
import asyncio
import logging
import os
import sys
from pathlib import Path

# Add parent directory to path for gllm_evals imports
PARENT_DIR = Path(__file__).parent.parent
if str(PARENT_DIR) not in sys.path:
    sys.path.insert(0, str(PARENT_DIR))

from experiment_fewshot_metric_level.config import get_experiment_config, get_fewshot_json_path
from experiment_fewshot_metric_level.evaluator import run_experiment
from experiment_fewshot_metric_level.utils import (
    add_retrieved_context,
    filter_by_fewshot_availability,
    filter_by_question_ids,
    load_experiment_data,
    load_fewshot_data,
    print_experiment_info,
    print_results_summary,
    remove_existing_predictions,
    save_results,
    save_summary,
)


def setup_logging() -> None:
    """Configure logging to suppress INFO messages."""
    logging.basicConfig(level=logging.WARNING, force=True)

    for logger_name in [
        "gllm_evals",
        "gllm_inference",
        "gllm_core",
        "openai",
        "httpx",
        "google",
        "anthropic",
    ]:
        logging.getLogger(logger_name).setLevel(logging.WARNING)
        logging.getLogger(logger_name).propagate = False


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Run few-shot evaluation experiment with metric-level few-shot support",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--experiment-index",
        type=str,
        default="0",
        help="Experiment configuration index - can be int (0, 1, 2...) or string name (botanica, botanica_test)",
    )

    parser.add_argument(
        "--eval-model",
        type=str,
        default="google/gemini-3-flash-preview",
        help="Model for evaluation. Default: google/gemini-3-flash-preview",
    )

    parser.add_argument(
        "--workers",
        type=int,
        default=5,
        help="Number of parallel workers. Default: 5",
    )

    parser.add_argument(
        "--question-ids",
        type=int,
        nargs="+",
        default=None,
        help="Specific question IDs to evaluate. Default: all questions",
    )

    parser.add_argument(
        "--use-small-data",
        action="store_true",
        help="Use small dataset for testing. Default: False",
    )

    parser.add_argument(
        "--fewshot-json",
        type=str,
        default=None,
        help="Path to few-shot examples JSON. Default: auto-detect",
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        default="./output",
        help="Output directory for results. Default: ./output",
    )

    parser.add_argument(
        "--fewshot-mode",
        type=str,
        choices=["append", "replace"],
        default="replace",
        help="Few-shot mode: 'append' or 'replace'. Default: replace",
    )

    return parser.parse_args()


async def main() -> None:
    """Main execution function."""
    args = parse_arguments()

    setup_logging()

    print("=" * 80)
    print("FEW-SHOT EXPERIMENT (METRIC-LEVEL)")
    print("=" * 80)
    print()

    try:
        experiment_config = get_experiment_config(args.experiment_index)
    except ValueError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

    fewshot_json_path = args.fewshot_json or get_fewshot_json_path(args.use_small_data)

    print(f"📂 Loading few-shot examples from: {fewshot_json_path}")

    try:
        fewshot_data = load_fewshot_data(fewshot_json_path)
        print(f"✅ Loaded few-shot data for {len(fewshot_data)} questions\n")
    except (FileNotFoundError, Exception) as e:
        print(f"❌ Error loading few-shot data: {e}")
        sys.exit(1)

    # Handle both 'data_path' and 'path' keys for backwards compatibility
    csv_path = Path(experiment_config.get("data_path") or experiment_config.get("path"))

    if args.use_small_data:
        small_csv_path = csv_path.parent / f"small_{csv_path.name}"
        if small_csv_path.exists():
            csv_path = small_csv_path
            print(f"✅ Using small dataset: {csv_path.name}")
        else:
            print(f"⚠️  Small dataset not found, using full dataset")

    print(f"📂 Loading experiment data from: {csv_path}")

    try:
        df = load_experiment_data(csv_path)
        print(f"✅ Loaded experiment data: {len(df)} rows\n")
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

    original_count = len(df)
    df = filter_by_fewshot_availability(df, fewshot_data)
    print(f"🔍 Filtered to {len(df)} rows with few-shot examples (from {original_count})")

    if args.question_ids is not None:
        before_filter = len(df)
        df = filter_by_question_ids(df, args.question_ids)
        print(f"🔍 Filtered to {len(df)} rows for question IDs: {sorted(args.question_ids)} (from {before_filter})")

    if len(df) == 0:
        print("❌ No rows to evaluate after filtering")
        sys.exit(1)

    df = add_retrieved_context(df, fewshot_data)
    print(f"✅ Added/verified 'retrieved_context' column")

    df = remove_existing_predictions(df)
    print(f"✅ Removed existing prediction columns\n")

    print_experiment_info(
        experiment_config,
        args.eval_model,
        args.workers,
        len(df),
        args.question_ids,
        args.fewshot_mode,
    )

    try:
        results_df = await run_experiment(
            df,
            fewshot_data,
            args.eval_model,
            args.workers,
            args.fewshot_mode,
        )
    except Exception as e:
        print(f"\n❌ Error during evaluation: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)

    print_results_summary(results_df, experiment_config)

    experiment_name = f"experiment_{experiment_config['index']}"

    output_path = save_results(
        results_df,
        args.output_dir,
        experiment_name,
        args.question_ids,
    )

    print(f"\n💾 Results saved to: {output_path}")

    summary = {
        "experiment_index": experiment_config["index"],
        "model_provider": experiment_config["model_provider"],
        "provider_model_id": experiment_config.get("provider_model_id", experiment_config.get("model_id", "unknown")),
        "eval_model": args.eval_model,
        "workers": args.workers,
        "total_rows": len(results_df),
        "question_ids": args.question_ids,
        "fewshot_mode": args.fewshot_mode,
        "output_file": str(output_path),
    }

    summary_path = save_summary(summary, args.output_dir, experiment_name)
    print(f"💾 Summary saved to: {summary_path}")

    print("\n" + "=" * 80)
    print("✅ EXPERIMENT COMPLETED SUCCESSFULLY!")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())
