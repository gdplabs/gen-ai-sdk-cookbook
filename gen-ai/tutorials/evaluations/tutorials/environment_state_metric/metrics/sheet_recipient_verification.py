"""Cross-checks who real sent emails went to against the recipient-mapping sheet.

Pure comparator: reads ``actual_sheet``, ``actual_emails``, and
``expected_recipients`` from the row.
"""

from __future__ import annotations

from typing import Any

from gllm_evals.metrics.metric import BaseMetric
from gllm_evals.types import LLMTestCase, MetricScore

from metrics._email_query import match_entry_in_pool, subject_terms
from metrics._row_fields import (
    actual_emails,
    actual_sheet,
    expected_emails,
    expected_recipients,
    oracle_error,
)


class _SuiteMisconfigError(Exception):
    """The suite's own config is wrong (e.g. a sender not in the mapping sheet)."""


# Recipients that may legitimately appear on a sent email without being in the
# mapping sheet, on top of the checked senders themselves.
_DEFAULT_RECIPIENT_ALLOWLIST = ("agent@example.com",)


class SheetRecipientVerificationMetric(BaseMetric):
    """Cross-checks that mapped recipients of report emails were actually emailed.

    Reads two ad hoc row fields:
    - ``expected_recipients`` (dict): ``{"spreadsheet_id": str, "sheet_range":
      str, "senders": list[str]}`` -- which recipient-mapping sheet to read,
      and which sender emails (from the test roster) to check. Optional keys:
      ``subject`` and ``allow_extra_recipients``.
    - ``actual_sheet``: the sender -> recipients mapping.
    - ``actual_emails``: the pre-fetched email pool, filtered by the subject
      rule to derive actual recipients.

    Conditional metric (``can_evaluate`` + inner skip-as-pass).

    Attributes:
        name: The metric name.
        type: Always ``"python"``.
        higher_is_better: Whether a higher score indicates better quality.
        threshold: Pass/fail threshold.
    """

    name = "sheet_recipient_verification"
    threshold = 1.0

    def can_evaluate(self, data: LLMTestCase) -> bool:
        """Check whether the row requests a recipient cross-check.

        Args:
            data: The materialized test case.

        Returns:
            True if ``expected_recipients`` is set on the row, False otherwise.
        """
        return bool(expected_recipients(data))

    async def _evaluate(self, data: LLMTestCase) -> MetricScore:
        """Verify expected recipients were emailed via the pre-fetched data.

        Args:
            data: The materialized test case, read for its
                ``expected_recipients``, ``actual_sheet``, and ``actual_emails``.

        Returns:
            A MetricScore of 1.0 if every mapped recipient received an email
            and no unexpected recipient was emailed; 0.0 with a diagnostic
            otherwise.
        """
        config = expected_recipients(data)
        if not config:
            return MetricScore(
                score=1.0,
                explanation="Row has no expected_recipients; skipping the sheet check.",
            )

        senders = config.get("senders") or []
        allowlist = {addr.strip().lower() for addr in senders if addr.strip()}
        allowlist |= {
            addr.strip().lower()
            for addr in (config.get("allow_extra_recipients") or ())
            if addr.strip()
        }
        allowlist |= set(_DEFAULT_RECIPIENT_ALLOWLIST)

        sheet_err = oracle_error(data, "sheet")
        mail_err = oracle_error(data, "mail")
        if sheet_err:
            return MetricScore(
                score=0.0,
                explanation=f"Live oracle read failed, cannot verify: sheet read failed: {sheet_err}",
            )
        if mail_err:
            return MetricScore(
                score=0.0,
                explanation=f"Live oracle read failed, cannot verify: mailbox read failed: {mail_err}",
            )

        mapping = actual_sheet(data)
        if mapping is None:
            return MetricScore(
                score=0.0,
                explanation="Oracle population did not retrieve the recipient-mapping sheet; cannot verify.",
            )

        try:
            expected = self._collect_expected_recipients(mapping, senders)
        except _SuiteMisconfigError as exc:
            return MetricScore(score=0.0, explanation=f"SUITE MISCONFIGURED (not an agent failure): {exc}")

        actual = self._fetch_actual_recipients(data, config)

        return self._score_result(expected, actual, senders, allowlist)

    def _collect_expected_recipients(
        self,
        mapping: dict[str, list[str]],
        senders: list[str],
    ) -> set[str]:
        """Collect the union of mapped recipients for the checked senders."""
        lowered_mapping = {
            sender.lower(): {r.strip().lower() for r in recipients if r.strip()}
            for sender, recipients in mapping.items()
        }
        expected: set[str] = set()
        for sender in senders:
            expected |= lowered_mapping.get(sender.lower(), set())

        if not expected:
            raise _SuiteMisconfigError(
                f"none of senders={senders} appear in the mapping sheet "
                f"(sheet has {len(mapping)} sender row(s)) -- check expected_recipients.spreadsheet_id / "
                f"sheet_range / senders against the sheet the agent actually uses"
            )
        return expected

    def _subject_entry(self, data: LLMTestCase, config: dict) -> dict:
        """Resolve the ``expected_emails``-shaped subject rule to scope sent emails."""
        subject_cfg = config.get("subject")
        if subject_cfg:
            return {"subject": subject_cfg}
        emails = expected_emails(data)
        return emails[0] if emails else {}

    def _fetch_actual_recipients(self, data: LLMTestCase, config: dict) -> set[str]:
        """Derive actual recipients from the pre-fetched email pool."""
        entry = self._subject_entry(data, config)
        contains, _ = subject_terms(entry)
        if not contains:
            return set()

        pool = actual_emails(data)
        subject_matches = match_entry_in_pool(entry, pool)

        actual: set[str] = set()
        for email in subject_matches:
            to_field = email.get("to") or ""
            actual.update(
                addr.strip().lower()
                for addr in to_field.split(",")
                if addr.strip()
            )
        return actual

    def _score_result(
        self,
        expected: set[str],
        actual: set[str],
        senders: list[str],
        allowlist: set[str],
    ) -> MetricScore:
        """Compare expected vs actual recipients and return the final score."""
        missing = expected - actual
        unexpected = actual - expected - allowlist
        if not missing and not unexpected:
            return MetricScore(
                score=1.0,
                explanation=(
                    f"All {len(expected)} mapped recipient(s) for senders={senders} received an email, "
                    f"with no unexpected recipients."
                ),
            )

        problems: list[str] = []
        if missing:
            problems.append(f"mapped recipient(s) with no email: {sorted(missing)}")
        if unexpected:
            problems.append(f"unexpected recipient(s) emailed: {sorted(unexpected)}")
        return MetricScore(
            score=0.0,
            explanation=(
                f"Recipient mismatch for senders={senders}. {'; '.join(problems)}. "
                f"Actual recipients seen: {sorted(actual)}."
            ),
        )


__all__ = ["SheetRecipientVerificationMetric"]
