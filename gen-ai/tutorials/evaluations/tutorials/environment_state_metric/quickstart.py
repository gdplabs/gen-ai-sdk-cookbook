import asyncio
import re
from typing import Any

from gllm_evals.dataset import DictDataset
from gllm_evals.metrics import BaseMetric
from gllm_evals.types import LLMTestCase, MetricScore

LABEL_MAP = {"PASS": "TRUE", "FAIL": "FALSE"}


def _has_term(text: str, term: str) -> bool:
    """Check if a specific term exists in the given text.

    Args:
        text (str): The text to search within.
        term (str): The term to search for.

    Returns:
        bool: True if the term is found, False otherwise.
    """
    return re.search(rf"\b{re.escape(term)}\b", text, re.IGNORECASE) is not None


class EmailSentVerificationMetric(BaseMetric):
    """Check that each expected email exists in the captured mailbox state.

    Attributes:
        name (str): Name of the metric.
        type (str): Type of the metric.
        higher_is_better (bool): Whether higher score is better.
        threshold (float): Threshold for the metric.
    """

    name = "email_sent_verification"
    type = "python"
    higher_is_better = True
    threshold = 1.0

    @staticmethod
    def _entry_matches(entry: dict[str, Any], email: dict[str, Any]) -> bool:
        """Check if an email matches the expected entry rules.

        Args:
            entry (dict[str, Any]): The expected entry rules containing subject, content, and to fields.
            email (dict[str, Any]): The observed email to check.

        Returns:
            bool: True if the email matches the entry rules, False otherwise.
        """
        subject = email.get("subject") or ""
        subject_rules = entry.get("subject") or {}
        if not all(_has_term(subject, term) for term in subject_rules.get("contains", [])):
            return False
        if any(_has_term(subject, term) for term in subject_rules.get("excludes", [])):
            return False

        body = email.get("body") or ""
        if not all(term in body for term in (entry.get("content") or {}).get("contains", [])):
            return False

        wanted = {address.lower() for address in (entry.get("to") or {}).get("contains", [])}
        actual = {address.strip().lower() for address in (email.get("to") or "").split(",") if address.strip()}
        return wanted <= actual

    async def _evaluate(self, data: LLMTestCase) -> MetricScore:
        """Evaluate the test case against the expected emails.

        Args:
            data (LLMTestCase): The test case containing expected and actual emails.

        Returns:
            MetricScore: The score and explanation of the evaluation.
        """
        expected = getattr(data, "expected_emails", None) or []
        observed = getattr(data, "actual_emails", None) or []
        claimed: set[str] = set()
        results = []

        for index, entry in enumerate(expected):
            match = next(
                (email for email in observed if email["id"] not in claimed and self._entry_matches(entry, email)),
                None,
            )
            if match is None:
                results.append((False, f"entry[{index}]: FAIL - no unclaimed email matched"))
            else:
                claimed.add(match["id"])
                results.append((True, f"entry[{index}]: PASS - matched {match['id']}"))

        passed = all(ok for ok, _ in results)
        explanation = "; ".join(text for _, text in results)
        return MetricScore(score=1.0 if passed else 0.0, explanation=explanation)


async def main() -> None:
    """Run the quickstart evaluation for the environment state metric."""
    rows = DictDataset.from_jsonl("quickstart_cases.jsonl").load()
    metric = EmailSentVerificationMetric()
    correct = 0

    for row in rows:
        result = await metric.evaluate(row)
        expected_pass = LABEL_MAP[row.label] == "TRUE"
        correct += result.success == expected_pass
        print(
            f"{row.name}: expected={'PASS' if expected_pass else 'FAIL'}, "
            f"score={result.score}, success={result.success}"
        )
        print(f"  {result.explanation}")

    print(f"\nAgreement with labels: {correct}/{len(rows)} ({correct / len(rows):.0%})")


if __name__ == "__main__":
    asyncio.run(main())
