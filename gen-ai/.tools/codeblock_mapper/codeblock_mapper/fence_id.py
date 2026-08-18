"""Computes stable IDs for fenced code blocks in GitBook markdown pages.

Implements the ID grammar:

    <gitbook-relative-path-no-ext>#<heading-slug>[/<step-title-slug>][/<tab-title-slug>]:<ordinal>

GitBook pages carry the ID as a literal `<!-- codeblock-id: ... -->` HTML
comment immediately above each fence. When present, that marker is read and
used verbatim instead of recomputing the ID from heading/stepper/tab
structure. Pages without a marker fall back to computing the ID from the
page's heading/stepper/tab structure directly.

References:
    NONE
"""

from __future__ import annotations

import re
from dataclasses import dataclass

_HEADING_PATTERN = re.compile(r"^(#{2,3})\s+(.*\S)\s*$")
_STEP_START_PATTERN = re.compile(r"^\{%\s*step\s*%\}\s*$")
_STEP_END_PATTERN = re.compile(r"^\{%\s*endstep\s*%\}\s*$")
_TAB_START_PATTERN = re.compile(r'^\{%\s*tab\s+title="([^"]*)"\s*%\}\s*$')
_TAB_END_PATTERN = re.compile(r"^\{%\s*endtab\s*%\}\s*$")
_FENCE_PATTERN = re.compile(r"^(```|~~~)\s*([\w+-]*)\s*$")
_BOLD_TITLE_PATTERN = re.compile(r"^\*\*(.+?)\*\*$")
_MARKER_PATTERN = re.compile(r"^<!--\s*codeblock-id:\s*(\S+)\s*-->\s*$")


@dataclass
class CodeFence:
    """A fenced code block found on a GitBook page, with its computed ID.

    Attributes:
        fence_id (str): The computed or marker-derived ID of the fence.
        code (str): The raw code content inside the fence.
        language (str): The fence's declared language, e.g. "python".
        start_line (int): The 1-based line number of the fence's opening delimiter.
        end_line (int): The 1-based line number of the fence's closing delimiter.
    """

    fence_id: str
    code: str
    language: str
    start_line: int
    end_line: int


def slugify(text: str) -> str:
    """Slugifies text using GitBook's own heading and anchor slugification rules.

    Args:
        text (str): The text to slugify, such as a heading or a tab title.

    Returns:
        str: The lowercase, hyphen-separated slug.
    """
    normalized_text = text.strip().lower()
    normalized_text = re.sub(r"[^a-z0-9\s-]", "", normalized_text)
    normalized_text = re.sub(r"\s+", "-", normalized_text)
    normalized_text = re.sub(r"-+", "-", normalized_text)
    return normalized_text.strip("-")


def _strip_bold_markers(title: str) -> str:
    """Strips Markdown bold markers from a step title line.

    Args:
        title (str): The raw step title line, e.g. "**Create the step**".

    Returns:
        str: The title text without surrounding "**" markers.
    """
    bold_match = _BOLD_TITLE_PATTERN.match(title.strip())
    return bold_match.group(1) if bold_match else title.strip()


def parse_code_fences(markdown: str, gitbook_relative_path: str) -> list[CodeFence]:
    """Parses a GitBook page and computes the ID of every fenced code block.

    A page with no enclosing heading yet produces an empty heading-slug
    segment, e.g. `<path>#:1`. A fence with no enclosing step or tab simply
    omits those optional ID segments. Nested scopes (a step inside a tab, or
    a tab inside a step) are supported; the ID always renders the step
    segment before the tab segment, regardless of source nesting order.

    A `<!-- codeblock-id: ... -->` comment immediately preceding a fence
    (blank lines and GitBook block tags may sit in between) is read as that
    fence's ID verbatim, bypassing computation entirely. A marker-derived ID
    does not consume the ordinal counter for its scope, so unmarked sibling
    fences on a partially migrated page still number correctly.

    Args:
        markdown (str): The full markdown content of a GitBook page.
        gitbook_relative_path (str): The page's path relative to
            `gitbook/gen-ai-sdk/`, without extension, e.g.
            "guides/build-end-to-end-rag-pipeline/adding-document-references".

    Returns:
        list[CodeFence]: Every fenced code block on the page, in document order.
    """
    lines = markdown.splitlines()

    heading_slug = ""
    step_slug: str | None = None
    tab_slug: str | None = None
    is_step_title_pending = False
    pending_marker_id: str | None = None

    ordinal_counters: dict[tuple[str, str | None, str | None], int] = {}
    code_fences: list[CodeFence] = []

    is_in_fence = False
    fence_language = ""
    fence_start_line = 0
    fence_content_lines: list[str] = []

    for line_number, raw_line in enumerate(lines, start=1):
        line = raw_line.rstrip("\n")

        if is_in_fence:
            closing_fence_match = _FENCE_PATTERN.match(line.strip())
            if not closing_fence_match:
                fence_content_lines.append(raw_line)
                continue

            code = "\n".join(fence_content_lines)
            if pending_marker_id is not None:
                fence_id = pending_marker_id
            else:
                fence_id = _compute_fence_id(
                    gitbook_relative_path, heading_slug, step_slug, tab_slug, ordinal_counters
                )
            code_fences.append(CodeFence(
                fence_id=fence_id,
                code=code,
                language=fence_language,
                start_line=fence_start_line,
                end_line=line_number,
            ))
            is_in_fence = False
            fence_content_lines = []
            pending_marker_id = None
            continue

        stripped_line = line.strip()

        marker_match = _MARKER_PATTERN.match(stripped_line)
        if marker_match:
            pending_marker_id = marker_match.group(1)
            continue

        opening_fence_match = _FENCE_PATTERN.match(stripped_line)
        if opening_fence_match:
            is_in_fence = True
            fence_language = opening_fence_match.group(2)
            fence_start_line = line_number
            fence_content_lines = []
            is_step_title_pending = False
            continue

        heading_match = _HEADING_PATTERN.match(line)
        if heading_match:
            heading_slug = slugify(heading_match.group(2))
            step_slug = None
            tab_slug = None
            continue

        if _STEP_START_PATTERN.match(stripped_line):
            is_step_title_pending = True
            step_slug = None
            continue

        if _STEP_END_PATTERN.match(stripped_line):
            step_slug = None
            is_step_title_pending = False
            continue

        tab_start_match = _TAB_START_PATTERN.match(stripped_line)
        if tab_start_match:
            tab_slug = slugify(tab_start_match.group(1))
            continue

        if _TAB_END_PATTERN.match(stripped_line):
            tab_slug = None
            continue

        if is_step_title_pending and stripped_line:
            step_slug = slugify(_strip_bold_markers(stripped_line))
            is_step_title_pending = False
            continue

    return code_fences


def _compute_fence_id(
    gitbook_relative_path: str,
    heading_slug: str,
    step_slug: str | None,
    tab_slug: str | None,
    ordinal_counters: dict[tuple[str, str | None, str | None], int],
) -> str:
    """Computes a fence's ID from its position in the page's scope structure.

    Args:
        gitbook_relative_path (str): The page's path relative to `gitbook/gen-ai-sdk/`.
        heading_slug (str): The slug of the fence's nearest enclosing heading.
        step_slug (str | None): The slug of the fence's enclosing step title, if any.
        tab_slug (str | None): The slug of the fence's enclosing tab title, if any.
        ordinal_counters (dict[tuple[str, str | None, str | None], int]): Running
            per-scope ordinal counts, mutated in place.

    Returns:
        str: The computed fence ID.
    """
    scope = (heading_slug, step_slug, tab_slug)
    ordinal_counters[scope] = ordinal_counters.get(scope, 0) + 1
    ordinal = ordinal_counters[scope]

    fence_id = f"{gitbook_relative_path}#{heading_slug}"
    if step_slug:
        fence_id += f"/{step_slug}"
    if tab_slug:
        fence_id += f"/{tab_slug}"
    return f"{fence_id}:{ordinal}"
