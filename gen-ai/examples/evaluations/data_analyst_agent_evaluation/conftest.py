"""Pytest configuration for data analyst agent evaluation.

Provides dataset loading, filtering utilities, and result collection for
evaluating the data analyst agent.

Author:
    - Mikhael Chris (mikhael.chris@gdplabs.id)
"""

import asyncio
import csv
from pathlib import Path
from typing import Any

import pytest

from questions import load_dataset as load_dataset_from_gsheets

# =============================================================================
# Constants
# =============================================================================

CSV_COLUMNS = [
    "no",
    "query_id",
    "predicted",
    "expected",
    "match",
    "manual_rr",
    "failed",
]


# =============================================================================
# Module-level variables
# =============================================================================

_dataset: list[dict[str, Any]] = []


# =============================================================================
# Public API for test files
# =============================================================================


def get_dataset() -> list[dict[str, Any]]:
    """Load and cache dataset for use in explicit @pytest.mark.parametrize.

    This function loads data on first call and caches it. Use this when you want
    to use explicit parametrization at module level in test files.

    Returns:
        List of test case records loaded from Google Sheets.

    Example:
        >>> from conftest import get_dataset, filter_data
        >>> from evaluations.agent_evaluator import AgentEvaluator
        >>>
        >>> # Load and filter data at module level
        >>> test_cases, test_ids = filter_data(get_dataset(), query_ids=[1, 2, 3])
        >>>
        >>> @pytest.mark.parametrize("record", test_cases, ids=test_ids)
        >>> def test_my_evaluation(record):
        ...     evaluator = AgentEvaluator()
        ...     assert evaluator.metric_has_answer(record) is True

    Note:
        This loads ALL data from Google Sheets without any filtering.
    """
    global _dataset
    if not _dataset:
        # Load data on first call
        _dataset = asyncio.run(load_dataset_from_gsheets())
    return _dataset


def filter_data(
    data: list[dict[str, Any]],
    query_ids: int | list[int] | None = None,
    question_ids: int | list[int] | None = None,
) -> tuple[list[dict[str, Any]], list[str]]:
    """Filter dataset and return (cases, ids) tuple for pytest.mark.parametrize.

    Args:
        data: Dataset to filter (typically from load_dataset()).
        query_ids: Single query ID or list of query IDs to include.
        question_ids: Single question number or list of question numbers to include.

    Returns:
        Tuple of (filtered_cases, test_ids) suitable for @pytest.mark.parametrize.
        test_ids are formatted as "q{query_id}_no_{question_no}".

    Example:
        >>> # Filter by specific query IDs
        >>> cases, ids = filter_data(get_dataset(), query_ids=[1, 2, 3])
        >>>
        >>> # Filter by question numbers
        >>> cases, ids = filter_data(get_dataset(), question_ids=[10, 20])
        >>>
        >>> # Filter by both
        >>> cases, ids = filter_data(get_dataset(), query_ids=17, question_ids=[1, 2])
    """
    # Normalize to lists
    if isinstance(query_ids, int):
        query_ids = [query_ids]
    if isinstance(question_ids, int):
        question_ids = [question_ids]

    # Filter data
    filtered = data
    if query_ids is not None:
        filtered = [r for r in filtered if int(r["query_id"]) in query_ids]
    if question_ids is not None:
        filtered = [r for r in filtered if int(r["no"]) in question_ids]

    # Generate test IDs
    ids = [f"q{r['query_id']}_no_{r['no']}" for r in filtered]

    return filtered, ids


# =============================================================================
# Result collection and session hooks
# =============================================================================


class ResultCollector:
    """Collects and stores evaluation results for CSV export."""

    def __init__(self) -> None:
        self.results: list[dict[str, Any]] = []

    def add_result(
        self,
        *,
        no: int,
        query_id: int,
        predicted: str,
        expected: str,
        match: bool,
        manual_rr: str,
        failed: bool,
    ) -> None:
        """Add a single evaluation result.

        Args:
            no: Question number.
            query_id: Query identifier.
            predicted: Predicted verdict ("good" or "bad").
            expected: Expected verdict from manual review.
            match: Whether prediction matches expected.
            manual_rr: Manual resolution rate annotation.
            failed: Whether the test case failed.
        """
        self.results.append(
            {
                "no": no,
                "query_id": query_id,
                "predicted": predicted,
                "expected": expected,
                "match": match,
                "manual_rr": manual_rr,
                "failed": failed,
            }
        )


@pytest.fixture(scope="session")
def result_collector(request: pytest.FixtureRequest) -> ResultCollector:
    """Provide a result collector for the test session.

    Args:
        request: Pytest fixture request object.

    Returns:
        Configured ResultCollector instance.
    """
    collector = ResultCollector()
    request.config._eval_collector = collector
    return collector


def _print_summary(results: list[dict[str, Any]]) -> None:
    """Print per-query accuracy summary.

    Args:
        results: List of evaluation result dictionaries.
    """
    matches_by_query: dict[int, list[bool]] = {}
    for result in results:
        matches_by_query.setdefault(result["query_id"], []).append(result["match"])
    for query_id in sorted(matches_by_query):
        matches = matches_by_query[query_id]
        print(f"query_id {query_id:2d}: {sum(matches)}/{len(matches)} correct")
    total = len(results)
    correct = sum(r["match"] for r in results)
    print(f"Overall accuracy: {correct}/{total} ({correct / total * 100:.1f}%)")


def _write_results_csv(results: list[dict[str, Any]], path: Path) -> None:
    """Write results to CSV file.

    Args:
        results: List of evaluation result dictionaries.
        path: Target file path for CSV output.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(results)
    print(f"Results written to {path}")


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    """Export results to CSV after test session completes.

    Args:
        session: Pytest session object.
        exitstatus: Exit status code from test run.
    """
    print("\nRunning teardown with pytest sessionfinish...")
    collector: ResultCollector | None = getattr(session.config, "_eval_collector", None)
    if not collector or not collector.results:
        return

    sorted_results = sorted(collector.results, key=lambda r: (r["query_id"], r["no"]))
    _print_summary(sorted_results)
    _write_results_csv(
        sorted_results, Path(__file__).parent / "results" / "history_eval_results.csv"
    )
