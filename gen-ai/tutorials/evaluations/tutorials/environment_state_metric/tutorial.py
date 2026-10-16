import asyncio
import json

from gllm_evals import EvalSuite, evaluate_suites
from gllm_evals.aggregation import true_negative_rate, true_positive_rate
from gllm_evals.dataset import DictDataset
from gllm_evals.evaluator import CompositeEvaluator
from gllm_evals.metrics.metric import BaseMetric

from metrics import (
    DocsContentVerificationMetric,
    EmailSentVerificationMetric,
    SheetRecipientVerificationMetric,
)

# Map dataset labels ("PASS"/"FAIL") to evaluation boolean equivalents ("TRUE"/"FALSE")
LABEL_MAP = {"PASS": "TRUE", "FAIL": "FALSE"}


async def run_calibration_dataset(metric: BaseMetric, evaluator_name: str | None = None) -> None:
    """Run calibration across labelled test cases from dataset/calibration.jsonl using evaluate_suites.

    Args:
        metric: The verification metric instance to evaluate.
        evaluator_name: Optional name for the evaluator suite.
    """
    name = evaluator_name or getattr(metric, "name", "verification_metric")
    print(f"\n--- Running Calibration on Dataset: {metric.__class__.__name__} ({name}) ---")

    # Load dataset cases from dataset/calibration.jsonl
    dataset = DictDataset.from_jsonl("dataset/calibration.jsonl").load()

    # Map dataset labels ("PASS"/"FAIL") to evaluation boolean equivalents ("TRUE"/"FALSE")
    for case in dataset:
        if hasattr(case, "label") and case.label in LABEL_MAP:
            case.label = LABEL_MAP[case.label]

    evaluator = CompositeEvaluator(
        metrics=[metric],
        name=name,
    )

    # Run evaluations using evaluate_suites with true_positive_rate and true_negative_rate aggregators
    result = await evaluate_suites(
        suites=[
            EvalSuite(
                name=f"calibration_{name}",
                data=dataset,
                evaluators=[evaluator],
            ),
        ],
        dataset_name=f"calibration_{name}",
        run_aggregators=[true_positive_rate, true_negative_rate],
    )

    print()
    print(f"--- Calibration Run Aggregators ({name}) ---")
    print(f"Pooled Accuracy: {result.run_aggregators_result.get('accuracy')}")
    print(f"Pooled TPR:      {result.run_aggregators_result.get('true_positive_rate')}")
    print(f"Pooled TNR:      {result.run_aggregators_result.get('true_negative_rate')}")
    print()
    print(json.dumps(result.model_dump(), indent=2, default=repr))


async def main() -> None:
    """Run dataset calibration for the 3 environment state verification metrics."""
    # Example 1: EmailSentVerificationMetric
    # Verifies whether required emails were actually sent (checking subject, content, and recipients).
    print("=" * 80)
    print("Example 1: EmailSentVerificationMetric")
    print("=" * 80)
    email_metric = EmailSentVerificationMetric()
    await run_calibration_dataset(email_metric, evaluator_name="email_sent_verification")

    # Example 2: DocsContentVerificationMetric
    # Verifies that Google Docs created by the agent contain required sections and titles.
    print("=" * 80)
    print("Example 2: DocsContentVerificationMetric")
    print("=" * 80)
    docs_metric = DocsContentVerificationMetric()
    await run_calibration_dataset(docs_metric, evaluator_name="docs_content_verification")

    # Example 3: SheetRecipientVerificationMetric
    # Cross-checks sent-to addresses against the recipient-mapping Google Sheet.
    print("=" * 80)
    print("Example 3: SheetRecipientVerificationMetric")
    print("=" * 80)
    sheet_metric = SheetRecipientVerificationMetric()
    await run_calibration_dataset(sheet_metric, evaluator_name="sheet_recipient_verification")


# Entrypoint to run async main loop
if __name__ == "__main__":
    asyncio.run(main())
