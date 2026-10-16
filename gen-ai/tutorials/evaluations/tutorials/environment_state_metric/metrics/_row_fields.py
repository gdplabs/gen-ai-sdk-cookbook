"""Accessors for test case attributes attached to LLMTestCase."""

from __future__ import annotations

from typing import Any
from gllm_evals.types import LLMTestCase

ACTUAL_EMAILS: str = "actual_emails"
ACTUAL_DOCS: str = "actual_docs"
ACTUAL_SHEET: str = "actual_sheet"
ORACLE_ERRORS: str = "oracle_errors"
EXPECTED_DOC_ID: str = "expected_doc_id"
EXPECTED_DATE_RANGE: str = "expected_date_range"


def expected_emails(data: LLMTestCase) -> list[dict[str, Any]]:
    """Return the expected_emails rule list."""
    return getattr(data, "expected_emails", None) or []


def expected_recipients(data: LLMTestCase) -> dict[str, Any] | None:
    """Return the expected_recipients configuration dictionary."""
    return getattr(data, "expected_recipients", None) or None


def excluded_recipients(data: LLMTestCase) -> list[str]:
    """Return recipient addresses that must not receive any email."""
    return getattr(data, "excluded_recipients", None) or []


def expected_doc_id(data: LLMTestCase) -> str | None:
    """Return the expected Google Docs document id."""
    return getattr(data, EXPECTED_DOC_ID, None) or None


def expected_date_range(data: LLMTestCase) -> str | None:
    """Return the expected reporting period date range string."""
    return getattr(data, EXPECTED_DATE_RANGE, None) or None


def expected_docs_content(data: LLMTestCase) -> list[str]:
    """Return the row's explicit expected_docs_content override list."""
    return getattr(data, "expected_docs_content", None) or []


def expected_docs_title(data: LLMTestCase) -> list[str]:
    """Return the row's explicit expected_docs_title override list."""
    return getattr(data, "expected_docs_title", None) or []


def actual_emails(data: LLMTestCase) -> list[dict[str, Any]]:
    """Return the list of emails observed in the environment."""
    return getattr(data, ACTUAL_EMAILS, None) or []


def actual_docs(data: LLMTestCase) -> dict[str, dict[str, str]]:
    """Return the fetched doc content keyed by doc id."""
    return getattr(data, ACTUAL_DOCS, None) or {}


def actual_sheet(data: LLMTestCase) -> dict[str, list[str]] | None:
    """Return the sender-to-recipients mapping from the sheet."""
    return getattr(data, ACTUAL_SHEET, None) or None


def oracle_error(data: LLMTestCase, key: str) -> str | None:
    """Return error string from environment state retrieval, if any."""
    errors = getattr(data, ORACLE_ERRORS, None) or {}
    return errors.get(key) or None


__all__ = [
    "ACTUAL_EMAILS",
    "ACTUAL_DOCS",
    "ACTUAL_SHEET",
    "ORACLE_ERRORS",
    "EXPECTED_DOC_ID",
    "EXPECTED_DATE_RANGE",
    "expected_emails",
    "expected_recipients",
    "excluded_recipients",
    "expected_doc_id",
    "expected_date_range",
    "expected_docs_content",
    "expected_docs_title",
    "actual_emails",
    "actual_docs",
    "actual_sheet",
    "oracle_error",
]
