"""Verification metric for emails sent by an agent against an environment mailbox."""

from __future__ import annotations

from typing import Any
from gllm_evals.metrics import BaseMetric
from gllm_evals.types import LLMTestCase, MetricScore

from metrics._content_matching import check_content
from metrics._doc_links import extract_doc_id_from_html
from metrics._email_query import match_entry_in_pool
from metrics._row_fields import (
    actual_emails,
    excluded_recipients,
    expected_date_range,
    expected_emails,
    oracle_error,
)


class EmailSentVerificationMetric(BaseMetric):
    """Verifies that expected emails were sent and excluded recipients were not contacted."""

    name = "email_sent_verification"
    type = "python"
    threshold = 1.0

    @staticmethod
    def _find_best_content_match(
        subject_matches: list[dict[str, Any]],
        content_contains: list[str],
    ) -> tuple[dict[str, Any] | None, list[str]]:
        """Find the subject-matched email that best satisfies the content criteria."""
        if not content_contains:
            return subject_matches[0], []

        best_email: dict[str, Any] | None = None
        best_missing: list[str] | None = None
        for email in subject_matches:
            ok, missing = check_content(content_contains, email.get("body") or "")
            if ok:
                return email, []
            if best_missing is None or len(missing) < len(best_missing):
                best_email, best_missing = email, missing
        return best_email, best_missing or []

    def _evaluate_entry(
        self,
        index: int,
        entry: dict[str, Any],
        pool: list[dict[str, Any]],
        used_ids: set[str],
        date_range: str | None,
    ) -> tuple[bool, str]:
        """Verify one expected email rule against the email pool."""
        subject_cfg = entry.get("subject") or {}
        contains_terms = subject_cfg.get("contains") or []
        excluded_terms = subject_cfg.get("excludes") or []
        content_contains = (entry.get("content") or {}).get("contains") or []
        required_recipients = {
            addr.strip().lower() for addr in (entry.get("to") or {}).get("contains") or []
        }
        docs_cfg = entry.get("docs") or {}

        if not contains_terms:
            return False, f"entry[{index}]: FAIL - no subject.contains configured"

        try:
            subject_matches = match_entry_in_pool(entry, pool)
        except ValueError as exc:
            return False, f"entry[{index}]: FAIL - invalid content pattern: {exc}"

        subject_matches = [email for email in subject_matches if email.get("id") not in used_ids]

        if not subject_matches:
            return False, (
                f"entry[{index}]: FAIL - no unclaimed email matched subject "
                f"contains={contains_terms} excludes={excluded_terms}"
            )

        try:
            matched_email, missing = self._find_best_content_match(subject_matches, content_contains)
        except ValueError as exc:
            return False, f"entry[{index}]: FAIL - invalid regex pattern: {exc}"

        if missing:
            return False, (
                f"entry[{index}]: FAIL - subject matched ({matched_email.get('id')}) but "
                f"content missing: {missing}"
            )

        assert matched_email is not None

        if required_recipients:
            actual_to = {
                addr.strip().lower()
                for addr in (matched_email.get("to") or "").split(",")
                if addr.strip()
            }
            missing_to = required_recipients - actual_to
            if missing_to:
                return False, (
                    f"entry[{index}]: FAIL - subject matched ({matched_email.get('id')}) but missing "
                    f"recipient(s) {sorted(missing_to)}"
                )

        if date_range:
            haystack = f"{matched_email.get('subject') or ''} {matched_email.get('body') or ''}"
            if date_range not in haystack:
                return False, (
                    f"entry[{index}]: FAIL - subject matched ({matched_email.get('id')}) but missing "
                    f"expected date range {date_range!r}"
                )

        if docs_cfg:
            doc_id = extract_doc_id_from_html(matched_email.get("body_html") or "")
            if not doc_id:
                return False, (
                    f"entry[{index}]: FAIL - subject matched ({matched_email.get('id')}) but "
                    f"email body has no Google Docs link"
                )

        used_ids.add(matched_email["id"])
        return True, f"entry[{index}]: PASS - matched {matched_email['id']} ({matched_email.get('subject')!r})"

    @staticmethod
    def _check_excluded(pool: list[dict[str, Any]], excluded: set[str]) -> tuple[bool, str]:
        """Check if any excluded recipient received an email."""
        hits = {
            email.get("id", "?"): sorted(addrs)
            for email in pool
            if (addrs := {a.strip().lower() for a in (email.get("to") or "").split(",") if a.strip()} & excluded)
        }
        if hits:
            return False, f"excluded recipient(s) reached -- {hits}"
        return True, f"none of the excluded recipient(s) received any email"

    async def _evaluate(self, data: LLMTestCase) -> MetricScore:
        """Evaluate if observed mailbox emails satisfy expected email rules."""
        emails = expected_emails(data)
        excluded = {addr.strip().lower() for addr in excluded_recipients(data) if addr.strip()}

        if not emails and not excluded:
            return MetricScore(
                score=1.0,
                explanation="No expected_emails or excluded_recipients to check.",
            )

        err = oracle_error(data, "mail")
        if err:
            return MetricScore(score=0.0, explanation=f"Mailbox read error: {err}")

        pool = actual_emails(data)
        date_range = expected_date_range(data)

        used_ids: set[str] = set()
        results = [
            self._evaluate_entry(index, entry, pool, used_ids, date_range)
            for index, entry in enumerate(emails)
        ]
        if excluded:
            results.append(self._check_excluded(pool, excluded))

        all_passed = all(passed for passed, _ in results)
        explanation = "; ".join(text for _, text in results)
        return MetricScore(
            score=1.0 if all_passed else 0.0,
            explanation=explanation,
        )


__all__ = ["EmailSentVerificationMetric"]
