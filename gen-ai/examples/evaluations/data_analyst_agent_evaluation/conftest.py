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


def pytest_configure(config: pytest.Config) -> None:
    """Initialize result collector at session start.

    Args:
        config: Pytest configuration object.
    """
    config._eval_collector = ResultCollector()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call):
    """Automatically collect test results after each test runs.

    This hook captures test outcomes and stores them in the result collector
    without requiring manual fixture injection in test functions.

    Args:
        item: Test item being executed.
        call: Test call information.
    """
    outcome = yield
    report = outcome.get_result()

    # Only process test call phase (not setup/teardown)
    if report.when != "call":
        return

    # Get the result collector
    collector = getattr(item.config, "_eval_collector", None)
    if not collector:
        return

    # Extract record data from test parameters
    if "record" not in item.funcargs:
        return

    record = item.funcargs["record"]

    # Determine test outcome
    test_passed = report.outcome == "passed"

    # Extract failure reason from assertion error
    failed_reason = ""
    if not test_passed and report.longrepr:
        # Get the assertion error message
        if hasattr(report.longrepr, "reprcrash"):
            failed_reason = report.longrepr.reprcrash.message
        else:
            # Extract just the assertion message
            lines = str(report.longrepr).split("\n")
            for line in lines:
                if "AssertionError:" in line:
                    failed_reason = line.split("AssertionError:")[-1].strip()
                    break
            if not failed_reason and lines:
                failed_reason = lines[-1].strip()

        # Remove newlines and extra whitespace for clean CSV output
        failed_reason = " ".join(failed_reason.split())

    # Extract metrics from test (if available in record or calculate default)
    predicted = "good" if test_passed else "bad"
    expected = record.get("manual_rr", "")
    match = predicted == expected if expected else False

    # Record result
    collector.add_result(
        no=int(record["no"]),
        query_id=int(record["query_id"]),
        predicted=predicted,
        expected=expected,
        match=match,
        manual_rr=expected,
        failed=failed_reason if failed_reason else (not test_passed),
    )


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
        failed: bool | str,
    ) -> None:
        """Add a single evaluation result.

        Args:
            no: Question number.
            query_id: Query identifier.
            predicted: Predicted verdict ("good" or "bad").
            expected: Expected verdict from manual review.
            match: Whether prediction matches expected.
            manual_rr: Manual resolution rate annotation.
            failed: False if passed, or failure message string if failed.
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
