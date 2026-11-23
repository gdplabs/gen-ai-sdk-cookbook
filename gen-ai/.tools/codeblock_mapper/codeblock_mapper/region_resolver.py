"""Resolves GitBook code fences to their matching region in the cookbook.

Matching is deterministic text comparison (difflib), never an LM call.

References:
    NONE
"""

from __future__ import annotations

import difflib
from dataclasses import dataclass
from pathlib import Path

from codeblock_mapper.fence_id import parse_code_fences

STATUS_IN_SYNC = "IN_SYNC"
STATUS_CONTENT_DRIFT = "CONTENT_DRIFT"
STATUS_UNMAPPED = "UNMAPPED"

UNMAPPED_COVERAGE_THRESHOLD = 0.3
IN_SYNC_COVERAGE_THRESHOLD = 0.98


@dataclass
class CookbookRegion:
    """A matched region inside a cookbook Python file.

    Attributes:
        file_path (Path): The cookbook file the region was matched in.
        start_line (int): The 1-based first line of the matched region.
        end_line (int): The 1-based last line of the matched region.
    """

    file_path: Path
    start_line: int
    end_line: int


def _normalize_lines(text: str) -> list[str]:
    """Strips and drops blank lines from text, for whitespace-insensitive matching.

    Args:
        text (str): The text to normalize.

    Returns:
        list[str]: The non-blank, stripped lines, in order.
    """
    return [line.strip() for line in text.splitlines() if line.strip()]


def find_matching_region(code: str, cookbook_directory: Path) -> tuple[CookbookRegion | None, float]:
    """Locates the region inside a cookbook directory's Python files matching `code`.

    Args:
        code (str): The fence content to search for.
        cookbook_directory (Path): The cookbook entry directory to search within.

    Returns:
        tuple[CookbookRegion | None, float]: The best-matching region and its
            coverage ratio (the fraction of the fence's non-blank lines found,
            in order, within the matched region), or (None, 0.0) if no Python
            files exist or nothing matches well enough to be worth reporting.
    """
    fence_lines = _normalize_lines(code)
    if not fence_lines:
        return None, 0.0

    candidate_files = sorted(
        file_path for file_path in cookbook_directory.glob("*.py")
        if not file_path.name.startswith("_")
    )
    best_region: CookbookRegion | None = None
    best_coverage_ratio = 0.0

    for candidate_file in candidate_files:
        region, coverage_ratio = _find_best_match_in_file(fence_lines, candidate_file)
        if region is None or coverage_ratio <= best_coverage_ratio:
            continue
        best_region = region
        best_coverage_ratio = coverage_ratio

    if best_region is None or best_coverage_ratio < UNMAPPED_COVERAGE_THRESHOLD:
        return None, best_coverage_ratio
    return best_region, best_coverage_ratio


def _find_best_match_in_file(fence_lines: list[str], file_path: Path) -> tuple[CookbookRegion | None, float]:
    """Finds the best-matching region for `fence_lines` within a single file.

    The non-blank line positions and the normalized lines used for matching
    must stay index-aligned, since matched indices are mapped back to
    original file line numbers through the same position list.

    Args:
        fence_lines (list[str]): The fence's normalized, non-blank lines.
        file_path (Path): The cookbook file to search within.

    Returns:
        tuple[CookbookRegion | None, float]: The matched region and its
            coverage ratio, or (None, 0.0) if no match was found.
    """
    file_lines = file_path.read_text().splitlines()
    non_blank_positions = [index for index, line in enumerate(file_lines) if line.strip()]
    if not non_blank_positions:
        return None, 0.0

    non_blank_file_lines = [file_lines[index].strip() for index in non_blank_positions]
    matcher = difflib.SequenceMatcher(None, non_blank_file_lines, fence_lines, autojunk=False)
    matching_blocks = [block for block in matcher.get_matching_blocks() if block.size > 0]
    if not matching_blocks:
        return None, 0.0

    matched_line_count = sum(block.size for block in matching_blocks)
    coverage_ratio = matched_line_count / len(fence_lines)

    match_start_index = min(block.a for block in matching_blocks)
    match_end_index = max(block.a + block.size for block in matching_blocks) - 1
    last_index = len(non_blank_positions) - 1
    start_line = non_blank_positions[min(match_start_index, last_index)] + 1
    end_line = non_blank_positions[min(match_end_index, last_index)] + 1

    return CookbookRegion(file_path=file_path, start_line=start_line, end_line=end_line), coverage_ratio


def classify_fence(code: str, cookbook_directory: Path) -> tuple[str, CookbookRegion | None]:
    """Classifies a fence as IN_SYNC, CONTENT_DRIFT, or UNMAPPED.

    Args:
        code (str): The fence content to classify.
        cookbook_directory (Path): The cookbook entry directory to match against.

    Returns:
        tuple[str, CookbookRegion | None]: The classification status and the
            matched region, if any.
    """
    region, coverage_ratio = find_matching_region(code, cookbook_directory)
    if region is None:
        return STATUS_UNMAPPED, None

    region_text = "\n".join(
        region.file_path.read_text().splitlines()[region.start_line - 1:region.end_line]
    )
    is_exact_match = _normalize_lines(code) == _normalize_lines(region_text)
    if coverage_ratio >= IN_SYNC_COVERAGE_THRESHOLD and is_exact_match:
        return STATUS_IN_SYNC, region
    return STATUS_CONTENT_DRIFT, region


def map_page_fences(
    markdown: str,
    gitbook_relative_path: str,
    cookbook_directory: Path,
    cookbook_root: Path,
) -> list[dict[str, str]]:
    """Computes the ID and cookbook-region resolution for every fence on a page.

    Args:
        markdown (str): The full markdown content of a GitBook page.
        gitbook_relative_path (str): The page's path relative to `gitbook/gen-ai-sdk/`,
            without extension.
        cookbook_directory (Path): The cookbook entry directory mapped to this page.
        cookbook_root (Path): The cookbook repository's `gen-ai/` directory, used to
            render the matched file as a repository-relative path.

    Returns:
        list[dict[str, str]]: One row per fence, with keys "id", "cookbook_file",
            "cookbook_line_range", and "status".
    """
    rows: list[dict[str, str]] = []
    for code_fence in parse_code_fences(markdown, gitbook_relative_path):
        status, region = classify_fence(code_fence.code, cookbook_directory)
        cookbook_file = str(region.file_path.relative_to(cookbook_root)) if region else ""
        cookbook_line_range = f"{region.start_line}-{region.end_line}" if region else ""
        rows.append({
            "id": code_fence.fence_id,
            "cookbook_file": cookbook_file,
            "cookbook_line_range": cookbook_line_range,
            "status": status,
        })
    return rows
