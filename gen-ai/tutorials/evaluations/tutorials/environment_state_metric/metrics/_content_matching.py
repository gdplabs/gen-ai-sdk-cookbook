"""Content matching helpers supporting literal substrings and regex patterns."""

from __future__ import annotations

import re

_REGEX_WRAPPER = re.compile(r'^r"(.*)"$', re.DOTALL)


def matches_entry(entry: str, text: str) -> bool:
    """Apply one content rule against text (literal substring or regex).

    Args:
        entry: Literal substring or r"<pattern>" regex.
        text: Target text to check against.

    Returns:
        bool: True if entry matches text.
    """
    wrapped = _REGEX_WRAPPER.match(entry)
    if wrapped:
        try:
            return re.search(wrapped.group(1), text) is not None
        except re.error as exc:
            raise ValueError(f"invalid regex in content.contains entry {entry!r}: {exc}") from exc
    return entry in text


def check_content(contains: list[str], text: str) -> tuple[bool, list[str]]:
    """Check that all required terms or patterns match the text.

    Args:
        contains: List of required substrings or regex patterns.
        text: Target text to verify.

    Returns:
        tuple[bool, list[str]]: (True, []) if all match, else (False, missing_items).
    """
    missing = [entry for entry in contains if not matches_entry(entry, text)]
    return not missing, missing


__all__ = ["matches_entry", "check_content"]
