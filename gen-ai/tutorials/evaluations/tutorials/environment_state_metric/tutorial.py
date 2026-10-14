import asyncio
import json
from typing import List, Optional
from pydantic import BaseModel
from gllm_evals import EvalSuite, evaluate_suites
from gllm_evals.aggregation import true_negative_rate, true_positive_rate
from gllm_evals.dataset import DictDataset
from gllm_evals.evaluator import CompositeEvaluator
from gllm_evals.metrics import BaseMetric
from gllm_evals.types import LLMTestCase, MetricScore

# Map dataset labels ("PASS"/"FAIL") to evaluation boolean equivalents ("TRUE"/"FALSE")
LABEL_MAP = {"PASS": "TRUE", "FAIL": "FALSE"}


# ==============================================================================
# 1. Pydantic Schemas: Data structures for rule validation & email snapshots
# ==============================================================================

# Word matching rules: required keywords (contains) and forbidden keywords (excludes)
class ContainsExcludesRule(BaseModel):
    contains: List[str] = []
    excludes: List[str] = []


# Expected rule schema for a single email (subject and content criteria)
class ExpectedEmail(BaseModel):
    subject: Optional[ContainsExcludesRule] = None
    content: Optional[ContainsExcludesRule] = None


# Observed email snapshot schema captured from the mailbox after agent actions
class ActualEmail(BaseModel):
    id: str
    subject: str
    content: str


# ==============================================================================
# 2. Metric Definition: Custom metric subclassing BaseMetric
# ==============================================================================
class EmailSentVerificationMetric(BaseMetric):
    """Verifies if the emails sent by the agent match the expected rules."""

    # Metric metadata and pass/fail threshold configuration
    name = "email_sent_verification"
    type = "programmatic"
    higher_is_better = True  # Higher score indicates better quality (1.0 = perfect)
    threshold = 1.0  # Requires 100% rule compliance (score 1.0) to pass

    def _matches(self, expected: ExpectedEmail, actual: ActualEmail) -> bool:
        """Helper to verify if a single observed email satisfies a single expected rule."""

        # Subject validation: check required terms (contains) and forbidden terms (excludes)
        if expected.subject:
            for word in expected.subject.contains:
                if word not in actual.subject:
                    return False
            for word in expected.subject.excludes:
                if word in actual.subject:
                    return False

        # Content/body validation: check required terms (contains) and forbidden terms (excludes)
        if expected.content:
            for word in expected.content.contains:
                if word not in actual.content:
                    return False
            for word in expected.content.excludes:
                if word in actual.content:
                    return False

        # All criteria satisfied
        return True

    async def _evaluate(self, data: LLMTestCase) -> MetricScore:
        """Core evaluation logic: matches expected rule set against actual emails."""

        # Step 1: Extract expected rules from test case into Pydantic models
        expected_data = getattr(data, "expected_emails", []) or []
        expected_emails = [ExpectedEmail(**rule) for rule in expected_data]

        # Step 2: Extract observed emails from mailbox state and normalize fields ('content'/'body')
        actual_data = getattr(data, "actual_emails", []) or []
        actual_emails = [
            ActualEmail(
                id=email.get("id", ""),
                subject=email.get("subject", ""),
                content=email.get("content") or email.get("body", ""),
            )
            for email in actual_data
        ]

        results = []
        # Track email IDs that have already matched a rule to prevent double-counting
        already_matched_ids: set[str] = set()

        # Step 3: Iterate through each expected rule and find an unused matching email
        for idx, expected in enumerate(expected_emails):
            match_found = False
            for actual in actual_emails:
                # Check for an email that hasn't been matched yet and satisfies _matches conditions
                if actual.id not in already_matched_ids and self._matches(expected, actual):
                    already_matched_ids.add(actual.id)  # Mark email ID as already matched
                    match_found = True
                    results.append(f"entry[{idx}]: PASS - matched msg {actual.id}")
                    break

            # If no matching email is found for this rule
            if not match_found:
                results.append(f"entry[{idx}]: FAIL - no email matched subject={expected.subject}")

        # Step 4: Determine pass/fail status (success only if results exist and all passed)
        success = len(results) > 0 and all("PASS" in r for r in results)
        score = 1.0 if success else 0.0

        # Step 5: Return MetricScore with numeric score and detailed explanation log
        return MetricScore(
            score=score,
            explanation="; ".join(results),
        )


# ==============================================================================
# 3. Main Runner: Dataset calibration using evaluate_suites
# ==============================================================================
async def run_calibration_dataset(metric: EmailSentVerificationMetric) -> None:
    """Run calibration across labelled test cases from dataset/calibration.jsonl using evaluate_suites and run_aggregators."""
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
