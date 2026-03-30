"""Pytest configuration: data loading, parameterization, result collection, CSV output."""

import asyncio
import csv
from pathlib import Path

import pytest

from questions import load_dataset


# ---------------------------------------------------------------------------
# Module-level dataset cache (populated once during collection)
# ---------------------------------------------------------------------------

_cached_dataset: dict[int, list[dict]] | None = None


def _parse_ids(value: str | None) -> set[int] | None:
    if not value:
        return None
    return {int(v.strip()) for v in value.split(",") if v.strip()}


def _get_dataset(config) -> dict[int, list[dict]]:
    global _cached_dataset
    if _cached_dataset is not None:
        return _cached_dataset

    query_ids = _parse_ids(config.getoption("--query-id"))
    question_ids = _parse_ids(config.getoption("--question-id"))

    records = asyncio.run(load_dataset(query_ids=query_ids, question_ids=question_ids))
    print(f"\nLoaded {len(records)} records")

    grouped: dict[int, list[dict]] = {}
    for r in records:
        grouped.setdefault(int(r["query_id"]), []).append(r)

    _cached_dataset = grouped
    return _cached_dataset


# ---------------------------------------------------------------------------
# CLI options
# ---------------------------------------------------------------------------


def pytest_addoption(parser):
    parser.addoption(
        "--query-id",
        default=None,
        metavar="IDS",
        help="Comma-separated query_id(s) to filter on (e.g. 1,3,5)",
    )
    parser.addoption(
        "--question-id",
        default=None,
        metavar="IDS",
        help="Comma-separated question no(s) to filter on (e.g. 10,20)",
    )


# ---------------------------------------------------------------------------
# Dynamic parameterization
# ---------------------------------------------------------------------------


def pytest_generate_tests(metafunc):
    if "record" not in metafunc.fixturenames:
        return
    query_id = getattr(metafunc.cls, "QUERY_ID", None)
    if query_id is None:
        return
    dataset = _get_dataset(metafunc.config)
    records = dataset.get(query_id, [])
    if not records:
        metafunc.parametrize(
            "record",
            [
                pytest.param(
                    None, marks=pytest.mark.skip(reason="no records for this query_id")
                )
            ],
        )
    else:
        ids = [f"no_{r['no']}" for r in records]
        metafunc.parametrize("record", records, ids=ids)


# ---------------------------------------------------------------------------
# Result collector
# ---------------------------------------------------------------------------

RESULT_FIELDS = [
    "no",
    "query_id",
    "predicted",
    "expected",
    "match",
    "manual_rr",
    "failed",
]


class EvalResultCollector:
    def __init__(self):
        self.results: list[dict] = []

    def add(self, *, no, query_id, predicted, expected, match, manual_rr, failed):
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
def result_collector(request):
    collector = EvalResultCollector()
    request.config._eval_collector = collector
    return collector


# ---------------------------------------------------------------------------
# Session finish: print summary + write CSV
# ---------------------------------------------------------------------------


def _print_summary(results: list[dict]) -> None:
    per_query: dict[int, list[bool]] = {}
    for r in results:
        per_query.setdefault(r["query_id"], []).append(r["match"])

    for qid in sorted(per_query):
        matches = per_query[qid]
        print(f"query_id {qid:2d}: {sum(matches)}/{len(matches)} correct")

    total = len(results)
    correct = sum(r["match"] for r in results)
    print(f"Overall accuracy: {correct}/{total} ({correct / total * 100:.1f}%)")


def _write_csv(results: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=RESULT_FIELDS)
        writer.writeheader()
        writer.writerows(results)
    print(f"Results written to {path}")


def pytest_sessionfinish(session, exitstatus):
    collector = getattr(session.config, "_eval_collector", None)
    if not collector or not collector.results:
        return

    results = sorted(collector.results, key=lambda r: (r["query_id"], r["no"]))
    _print_summary(results)
    _write_csv(results, Path(__file__).parent / "results" / "history_eval_results.csv")
