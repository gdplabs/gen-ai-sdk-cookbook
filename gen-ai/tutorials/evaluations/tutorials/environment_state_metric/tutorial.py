import asyncio
import json

from gllm_evals import EvalSuite, evaluate_suites
from gllm_evals.aggregation import true_negative_rate, true_positive_rate
from gllm_evals.dataset import DictDataset
from gllm_evals.evaluator import CompositeEvaluator

from metrics import EmailSentVerificationMetric

# Map dataset labels ("PASS"/"FAIL") to evaluation boolean equivalents ("TRUE"/"FALSE")
LABEL_MAP = {"PASS": "TRUE", "FAIL": "FALSE"}


async def run_calibration_dataset(metric: EmailSentVerificationMetric) -> None:
    """Run calibration across labelled test cases from dataset/calibration.jsonl using evaluate_suites."""
    print("--- Running Calibration on Dataset (dataset/calibration.jsonl) ---")

    # Load dataset cases from dataset/calibration.jsonl
    dataset = DictDataset.from_jsonl("dataset/calibration.jsonl").load()

    # Map dataset labels ("PASS"/"FAIL") to evaluation boolean equivalents ("TRUE"/"FALSE")
    for case in dataset:
        if hasattr(case, "label") and case.label in LABEL_MAP:
            case.label = LABEL_MAP[case.label]

    evaluator = CompositeEvaluator(
        metrics=[metric],
        name="email_sent_verification",
    )

    # Run evaluations using evaluate_suites with true_positive_rate and true_negative_rate aggregators
    result = await evaluate_suites(
        suites=[
            EvalSuite(
                name="calibration",
                data=dataset,
                evaluators=[evaluator],
            ),
        ],
        dataset_name="calibration",
        run_aggregators=[true_positive_rate, true_negative_rate],
    )

    print()
    print("--- Calibration Run Aggregators ---")
    print(f"Pooled Accuracy: {result.run_aggregators_result.get('accuracy')}")
    print(f"Pooled TPR:      {result.run_aggregators_result.get('true_positive_rate')}")
    print(f"Pooled TNR:      {result.run_aggregators_result.get('true_negative_rate')}")
    print()
    print(json.dumps(result.model_dump(), indent=2, default=repr))


async def main() -> None:
    """Run dataset calibration using evaluate_suites."""
    metric = EmailSentVerificationMetric()
    await run_calibration_dataset(metric)


# Entrypoint to run async main loop
if __name__ == "__main__":
    asyncio.run(main())
