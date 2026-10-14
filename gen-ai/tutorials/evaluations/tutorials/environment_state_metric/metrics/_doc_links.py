"""Google Docs link parsing helpers."""

from __future__ import annotations

import re

_DOC_LINK_RE = re.compile(r"https://docs\.google\.com/document/d/([a-zA-Z0-9_-]+)")


def extract_doc_id_from_html(body_html: str | None) -> str | None:
    """Extract the first Google Docs document id linked in HTML body.

    Args:
        body_html: Raw HTML string of the email body.

    Returns:
        str | None: Document id if found, else None.
    """
    match = _DOC_LINK_RE.search(body_html or "")
    return match.group(1) if match else None


__all__ = ["extract_doc_id_from_html"]
