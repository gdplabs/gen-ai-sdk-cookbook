"""Whole-word subject matching helpers."""

from __future__ import annotations

import re

_WORD_BOUNDARY_CACHE: dict[str, re.Pattern[str]] = {}


def match_whole_word(text: str, phrase: str) -> bool:
    """Perform case-insensitive whole-word or phrase matching.

    Args:
        text: Text to search within.
        phrase: Word or phrase that must appear on a word boundary.

    Returns:
        bool: True if phrase appears in text on a word boundary.
    """
    pattern = _WORD_BOUNDARY_CACHE.get(phrase)
    if pattern is None:
        pattern = re.compile(r"\b" + re.escape(phrase) + r"\b", re.IGNORECASE)
        _WORD_BOUNDARY_CACHE[phrase] = pattern
    return bool(pattern.search(text or ""))


def passes_inclusion_check(subject: str, contains_terms: list[str]) -> bool:
    """Check if all terms appear in subject as whole words or phrases."""
    return all(match_whole_word(subject, term) for term in contains_terms)


def passes_exclusion_check(subject: str, excluded_terms: list[str]) -> bool:
    """Check if none of the excluded terms appear in subject."""
    return not any(match_whole_word(subject, term) for term in excluded_terms)


__all__ = ["match_whole_word", "passes_inclusion_check", "passes_exclusion_check"]
