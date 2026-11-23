"""Email pool query and matching helpers."""

from __future__ import annotations

from typing import Any
from metrics._subject_matching import passes_exclusion_check, passes_inclusion_check


def subject_terms(entry: dict[str, Any]) -> tuple[list[str], list[str]]:
    """Extract (contains, excludes) term lists from an expected email subject rule.

    Args:
        entry: Expected email rule dictionary.

    Returns:
        tuple[list[str], list[str]]: (contains_terms, excludes_terms)
    """
    subject_cfg = entry.get("subject") or {}
    return (subject_cfg.get("contains") or [], subject_cfg.get("excludes") or [])


def match_entry_in_pool(
    entry: dict[str, Any],
    pool: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Filter email pool by matching the entry's subject inclusion and exclusion criteria.

    Args:
        entry: Expected email rule specification.
        pool: List of observed email dictionaries.

    Returns:
        list[dict[str, Any]]: Matching emails in pool order.
    """
    contains, excludes = subject_terms(entry)

    matches: list[dict[str, Any]] = []
    for email in pool:
        subj = email.get("subject") or ""
        if not passes_inclusion_check(subj, contains):
            continue
        if not passes_exclusion_check(subj, excludes):
            continue
        matches.append(email)

    return matches


__all__ = ["subject_terms", "match_entry_in_pool"]
