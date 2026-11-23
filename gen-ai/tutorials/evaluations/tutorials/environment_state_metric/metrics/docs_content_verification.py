"""Checks a Google Doc's content, independently of the agent's claimed response.

Pure comparator: reads ``actual_docs``, ``expected_doc_id``, and
``expected_date_range`` from the row and compares against
``expected_docs_content`` / ``expected_docs_title``.
"""

from __future__ import annotations

from gllm_evals.metrics.metric import BaseMetric
from gllm_evals.types import LLMTestCase, MetricScore

from metrics._content_matching import check_content
from metrics._row_fields import (
    actual_docs,
    expected_date_range,
    expected_doc_id,
    expected_docs_content,
    expected_docs_title,
    expected_emails,
    oracle_error,
)


def _docs_content_for(data: LLMTestCase) -> list[str]:
    """Find the ``content.contains`` list to check the doc against.

    Prefers an explicit ``expected_docs_content`` on the row (standalone
    testing). Otherwise, the content list is authored on the
    ``expected_emails`` entry that carries the ``docs`` block.

    Args:
        data: The materialized test case.

    Returns:
        The ``content.contains`` entries to check, or an empty list if none.
    """
    explicit = expected_docs_content(data)
    if explicit:
        return explicit

    for entry in expected_emails(data):
        docs_cfg = entry.get("docs")
        if docs_cfg:
            return (docs_cfg.get("content") or {}).get("contains") or []
    return []


def _docs_title_for(data: LLMTestCase) -> list[str]:
    """Find the ``title.contains`` list to check the doc's title against.

    Starts from an explicit ``expected_docs_title`` on the row, or the
    entry's authored ``docs.title.contains``. ``expected_date_range`` (a
    dynamic value) is always added on top when set, so any row with a
    resolved doc gets the reporting-period check for free.

    Args:
        data: The materialized test case.

    Returns:
        The title-check strings, or an empty list if none apply.
    """
    explicit = expected_docs_title(data)
    terms = list(explicit) if explicit else []

    if not terms:
        for entry in expected_emails(data):
            docs_cfg = entry.get("docs")
            if docs_cfg:
                terms = list((docs_cfg.get("title") or {}).get("contains") or [])
                break

    date_range = expected_date_range(data)
    if date_range and date_range not in terms:
        terms.append(date_range)

    return terms


class DocsContentVerificationMetric(BaseMetric):
    """Fail if the row's target Google Doc is missing any expected content.

    Reads ``expected_doc_id``, ``actual_docs``, and the expected content/title from the row.
    When the row carries ``expected_date_range``, the doc's title is also
    checked for it automatically.
    If oracle population recorded an error (``oracle_errors["docs"]``), the
    metric scores 0.0.

    Conditional metric (``can_evaluate`` + inner skip-as-pass).

    Attributes:
        name: The metric name.
        type: Always ``"python"``.
        higher_is_better: Whether a higher score indicates better quality.
        threshold: Pass/fail threshold.
    """

    name = "docs_content_verification"
    threshold = 1.0

    def can_evaluate(self, data: LLMTestCase) -> bool:
        """Check whether the row has a doc to verify or a docs failure to report.

        Args:
            data: The materialized test case.

        Returns:
            True if ``expected_doc_id`` is set on the row, or oracle errors
            recorded a ``docs`` error. False otherwise.
        """
        return bool(expected_doc_id(data)) or bool(oracle_error(data, "docs"))

    async def _evaluate(self, data: LLMTestCase) -> MetricScore:
        """Independently verify the doc contains the expected content.

        Args:
            data: The materialized test case, read for its ``expected_doc_id``,
                ``actual_docs``, and expected content/title.

        Returns:
            A MetricScore of 1.0 if the doc contains every expected string (or
            none were configured), or 0.0 if the doc read fails or any expected
            string is missing.
        """
        document_id = expected_doc_id(data)
        expected_contains = _docs_content_for(data)
        expected_title = _docs_title_for(data)

        err = oracle_error(data, "docs")
        if err:
            return MetricScore(score=0.0, explanation=f"Live docs read failed, cannot verify: {err}")

        if not document_id:
            return MetricScore(score=1.0, explanation="Row has no expected_doc_id; skipping the docs check.")

        doc = actual_docs(data).get(document_id)
        if not doc:
            return MetricScore(
                score=0.0,
                explanation=f"Target doc {document_id!r} was not retrieved during oracle population.",
            )

        title = doc.get("title", "")
        text = doc.get("text", "")

        if not expected_contains and not expected_title:
            return MetricScore(
                score=1.0,
                explanation=f"Doc {document_id!r} ({title!r}) fetched; nothing configured to check.",
            )

        try:
            title_ok, title_missing = check_content(expected_title, title)
            content_ok, content_missing = check_content(expected_contains, text)
        except ValueError as exc:
            return MetricScore(score=0.0, explanation=f"SUITE MISCONFIGURED (bad content.contains regex): {exc}")

        if title_ok and content_ok:
            return MetricScore(
                score=1.0,
                explanation=(
                    f"Doc {document_id!r} ({title!r}) matches: "
                    f"{len(expected_title)} title string(s), {len(expected_contains)} content string(s)."
                ),
            )
        problems = []
        if title_missing:
            problems.append(f"title missing {title_missing}")
        if content_missing:
            problems.append(f"content missing {content_missing}")
        return MetricScore(
            score=0.0,
            explanation=f"Doc {document_id!r} ({title!r}) failed: {'; '.join(problems)}.",
        )


__all__ = ["DocsContentVerificationMetric"]
