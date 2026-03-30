"""Pytest configuration for data analyst agent evaluation.

Loads test dataset, provides parameterized test cases, and collects results.
"""

import asyncio
import csv
from pathlib import Path
from typing import Any

import pytest

from questions import load_dataset

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
# Module-level variables (populated by pytest_configure)
# =============================================================================

_all_records: list[dict[str, Any]] = []
records_by_query: dict[int, list[dict[str, Any]]] = {}
TEST_CASES: list[dict[str, Any]] = []
TEST_IDS: list[str] = []

# =============================================================================
# Helper functions (used by hooks)
# =============================================================================


def _parse_comma_separated_ids(value: str | None) -> set[int] | None:
    """Parse comma-separated string into set of integers.

    Args:
        value: Comma-separated IDs string (e.g., "1,2,3") or None.

    Returns:
        Set of integer IDs, or None if input is empty/None.
    """
    if not value:
        return None
    return {int(v.strip()) for v in value.split(",") if v.strip()}


# =============================================================================
# Pytest hooks (in execution order: addoption -> configure -> sessionfinish)
# =============================================================================


def pytest_addoption(parser: pytest.Parser) -> None:
    """Add CLI options for filtering test cases.

    Args:
        parser: Pytest parser to add options to.
    """
    parser.addoption(
        "--query-id",
        default=None,
        metavar="IDS",
        help="Comma-separated query IDs (e.g. 1,3,5)",
    )
    parser.addoption(
        "--question-id",
        default=None,
        metavar="IDS",
        help="Comma-separated question numbers (e.g. 10,20)",
    )


def pytest_configure(config: pytest.Config) -> None:
    """Load and filter dataset based on CLI options.

    Args:
        config: Pytest configuration object with CLI options.
    """
    global _all_records, records_by_query, TEST_CASES, TEST_IDS

    query_ids = _parse_comma_separated_ids(config.getoption("--query-id"))
    question_ids = _parse_comma_separated_ids(config.getoption("--question-id"))

    _all_records = asyncio.run(
        load_dataset(query_ids=query_ids, question_ids=question_ids)
    )
    print(f"\nLoaded {len(_all_records)} records")

    # Group records by query_id for organized test execution
    records_by_query = {}
    for record in _all_records:
        query_id = int(record["query_id"])
        records_by_query.setdefault(query_id, []).append(record)

    # Flatten into ordered test cases
    TEST_CASES = [
        record
        for query_id in sorted(records_by_query.keys())
        for record in records_by_query[query_id]
    ]
    TEST_IDS = [f"q{r['query_id']}_no_{r['no']}" for r in TEST_CASES]


# =============================================================================
# Public API for test files
# =============================================================================


def get_test_cases_for_query(query_id: int) -> tuple[list[dict[str, Any]], list[str]]:
    """Return test cases and their display IDs for a specific query.

    Args:
        query_id: The query identifier to filter by.

    Returns:
        Tuple of (test_cases, test_ids) for the query.
    """
    cases = records_by_query.get(query_id, [])
    ids = [f"q{r['query_id']}_no_{r['no']}" for r in cases]
    return cases, ids


# =============================================================================
# Private helpers for sessionfinish
# =============================================================================


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
    collector: ResultCollector | None = getattr(session.config, "_eval_collector", None)
    if not collector or not collector.results:
        return
    sorted_results = sorted(collector.results, key=lambda r: (r["query_id"], r["no"]))
    _print_summary(sorted_results)
    _write_results_csv(
        sorted_results, Path(__file__).parent / "results" / "history_eval_results.csv"
    )


# =============================================================================
# Result collection classes and fixtures
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
