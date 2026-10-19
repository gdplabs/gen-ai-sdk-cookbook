import asyncio
import json

from gllm_evals import EvalSuite, evaluate_suites
from gllm_evals.aggregation import true_negative_rate, true_positive_rate
from gllm_evals.dataset import DictDataset
from gllm_evals.evaluator import CompositeEvaluator

from metrics import (
    DocsContentVerificationMetric,
    EmailSentVerificationMetric,
    SheetRecipientVerificationMetric,
)

# Map dataset labels ("PASS"/"FAIL") to evaluation boolean equivalents ("TRUE"/"FALSE")
LABEL_MAP = {"PASS": "TRUE", "FAIL": "FALSE"}


async def run_calibration() -> None:
    """Run calibration across test case suites using evaluate_suites in a single execution."""
    print("--- 1. Loading Calibration Dataset (dataset/calibration.jsonl) ---")
    dataset = DictDataset.from_jsonl("dataset/calibration.jsonl").load()

    # Map dataset labels ("PASS"/"FAIL") to evaluation boolean equivalents ("TRUE"/"FALSE")
    for case in dataset:
        if hasattr(case, "label") and case.label in LABEL_MAP:
            case.label = LABEL_MAP[case.label]

    # Group test cases by suite_name
    grouped_cases: dict[str, list] = {}
    for case in dataset:
        suite_name = getattr(case, "suite_name", None)
        if suite_name:
            grouped_cases.setdefault(suite_name, []).append(case)

    print(f"Loaded {len(dataset)} cases across {len(grouped_cases)} suites: {list(grouped_cases.keys())}")

    print("\n--- 2. Defining Evaluators and Building EvalSuites ---")
    # Define metrics per suite based on their test case YAML configurations:
    # - saturday-create: verifies emails sent and created doc content
    # - saturday-remind: verifies reminder emails and reminder doc title
    # - saturday-share:  verifies share emails and cross-checks sheet recipients
    suite_configs = {
        "saturday-create": [
            EmailSentVerificationMetric(),
            DocsContentVerificationMetric(),
        ],
        "saturday-remind": [
            EmailSentVerificationMetric(),
            DocsContentVerificationMetric(),
        ],
        "saturday-share": [
            EmailSentVerificationMetric(),
            SheetRecipientVerificationMetric(),
        ],
    }

    suites = []
    for suite_name, metrics in suite_configs.items():
        cases = grouped_cases.get(suite_name, [])
        evaluator = CompositeEvaluator(
            name=suite_name,
            metrics=metrics,
        )
        suites.append(
            EvalSuite(
                name=suite_name,
                data=cases,
                evaluators=[evaluator],
            )
        )

    print("\n--- 3. Running evaluate_suites across all suites ---")
    result = await evaluate_suites(
        suites=suites,
        dataset_name="weekly_report_calibration",
        run_aggregators=[true_positive_rate, true_negative_rate],
    )

    print("\n--- Calibration Run Aggregators ---")
    tpr = result.run_aggregators_result.get("true_positive_rate", {})
    tnr = result.run_aggregators_result.get("true_negative_rate", {})
    accuracy = result.run_aggregators_result.get("accuracy", {})

    print(f"{'Suite':<20} | {'TPR':<10} | {'TNR':<10} | {'Pass Rate (Accuracy)':<20}")
    print("-" * 70)
    for suite_name in suite_configs:
        suite_tpr = tpr.get(suite_name, "N/A")
        suite_tnr = tnr.get(suite_name, "N/A")
        suite_acc = accuracy.get(suite_name, "N/A")
        print(f"{suite_name:<20} | {str(suite_tpr):<10} | {str(suite_tnr):<10} | {str(suite_acc):<20}")

    print("\n--- Full Experiment Result Dump ---")
    print(json.dumps(result.model_dump(), indent=2, default=repr))


async def main() -> None:
    """Entry point for offline environment state metric calibration."""
    await run_calibration()


if __name__ == "__main__":
    asyncio.run(main())
