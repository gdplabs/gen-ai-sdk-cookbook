import asyncio
from typing import List, Optional
import yaml
from pydantic import BaseModel
from gllm_evals.metrics import BaseMetric
from gllm_evals.types import LLMTestCase, MetricScore
from gllm_evals.dataset import DictDataset

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
# 3. Main Runner: YAML test case evaluation & JSONL calibration
# ==============================================================================
async def run_yaml_suite(metric: EmailSentVerificationMetric) -> None:
    """Load test case rules directly from dataset/02_saturday_remind.yaml and evaluate."""
    print("--- [1] Evaluating Test Case from YAML (dataset/02_saturday_remind.yaml) ---")

    # Read and parse test case specification from YAML file
    with open("dataset/02_saturday_remind.yaml", "r") as f:
        yaml_config = yaml.safe_load(f)

    test_case_def = yaml_config["data"][0]
    expected_rules = test_case_def.get("expected_emails", [])

    # Scenario A: Simulated state where agent failed to send the email
    case_empty = LLMTestCase(
        name=f"{test_case_def['id']} (Empty Mailbox)",
        input=test_case_def["input"],
        expected_emails=expected_rules,
        actual_emails=[],
    )
    res_empty = await metric.evaluate(case_empty)
    print(f"Case: {case_empty.name}")
    print(f"  Result:  {'PASS' if res_empty.success else 'FAIL'} (score={res_empty.score})")
    print(f"  Details: {res_empty.explanation}\n")

    # Scenario B: Simulated state where agent successfully sent the reminder email
    case_success = LLMTestCase(
        name=f"{test_case_def['id']} (Reminder Sent)",
        input=test_case_def["input"],
        expected_emails=expected_rules,
        actual_emails=[
            {
                "id": "msg-001",
                "subject": "Reminder: Weekly Report Due",
                "body": "This is a friendly reminder to complete your weekly report before the due date.",
            }
        ],
    )
    res_success = await metric.evaluate(case_success)
    print(f"Case: {case_success.name}")
    print(f"  Result:  {'PASS' if res_success.success else 'FAIL'} (score={res_success.score})")
    print(f"  Details: {res_success.explanation}\n")


async def run_calibration_dataset(metric: EmailSentVerificationMetric) -> None:
    """Run calibration across labelled test cases from dataset/dataset.jsonl."""
    print("--- [2] Running Calibration on Dataset (dataset/dataset.jsonl) ---")

    # Load dataset cases from dataset.jsonl
    dataset = DictDataset.from_jsonl("dataset/dataset.jsonl").load()

    correct = 0
    for case in dataset:
        result = await metric.evaluate(case)

        expected_pass = LABEL_MAP[case.label] == "TRUE"
        correct += result.success == expected_pass

        print(f"Case: {case.name}")
        print(f"  Expected: {'PASS' if expected_pass else 'FAIL'}")
        print(f"  Result:   {'PASS' if result.success else 'FAIL'} (score={result.score})")
        print(f"  Details:  {result.explanation}\n")

    print(f"Calibration agreement: {correct}/{len(dataset)} ({correct / len(dataset):.0%})\n")


async def main() -> None:
    """Run both the YAML test suite and dataset calibration."""
    metric = EmailSentVerificationMetric()
    await run_yaml_suite(metric)
    await run_calibration_dataset(metric)


# Entrypoint to run async main loop
if __name__ == "__main__":
    asyncio.run(main())