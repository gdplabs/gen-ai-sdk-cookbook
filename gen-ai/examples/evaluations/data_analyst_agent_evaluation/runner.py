"""History-based evaluation runner."""

import argparse
import asyncio
import csv
import json
import logging
from pathlib import Path

from evaluators import EVALUATORS
from metrics import completeness_score
from questions import load_dataset

logging.basicConfig(level=logging.INFO, format="%(name)s - %(levelname)s - %(message)s")


RESULT_FIELDS = ["no", "query_id", "predicted", "expected", "match", "manual_rr", "failed"]


def parse_ids(value: str) -> list[int]:
    """Parse a comma-separated list of integers."""
    return [int(v.strip()) for v in value.split(",") if v.strip()]


def _evaluate_records(records: list[dict]) -> list[dict]:
    """Evaluate each record and return result dicts."""
    results = []
    for record in records:
        query_id = int(record["query_id"])
        evaluator = EVALUATORS[query_id]()
        predicted, metrics = evaluator.evaluate(record)
        failed_metrics = {name: result for name, result in metrics.items() if not result}
        expected = "good" if record["manual_rr"] == "good" else "bad"
        results.append(
            {
                "no": record["no"],
                "query_id": query_id,
                "predicted": predicted,
                "expected": expected,
                "match": predicted == expected,
                "manual_rr": record["manual_rr"],
                "failed": json.dumps(failed_metrics),
            }
        )
    return results


def _print_summary(results: list[dict]) -> None:
    """Print per-query and overall accuracy."""
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
    """Write evaluation results to a CSV file."""
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=RESULT_FIELDS)
        writer.writeheader()
        writer.writerows(results)
    print(f"Results written to {path}")


async def main() -> None:
    """Run history-based evaluation on AIP data analysis agent."""
    parser = argparse.ArgumentParser(description="Run AIP data analysis agent evaluation.")
    parser.add_argument(
        "--query-id",
        type=parse_ids,
        metavar="IDS",
        help="Comma-separated query_id(s) to filter on (e.g. 1,3,5)",
    )
    parser.add_argument(
        "--question-id",
        type=parse_ids,
        metavar="IDS",
        help="Comma-separated question no(s) to filter on (e.g. 10,20)",
    )
    args = parser.parse_args()

    query_ids = set(args.query_id) if args.query_id else None
    question_ids = set(args.question_id) if args.question_id else None
    records = await load_dataset(query_ids=query_ids, question_ids=question_ids)
    print(f"Loaded {len(records)} records")

    print("Pre-computing completeness scores...")
    scores = await completeness_score(records)
    for record, score in zip(records, scores):
        record["_completeness_score"] = score

    # print("Loading pre-computed completeness scores...")
    # from .completeness_result import completeness_result
    # scores = [item["generation"]["completeness"]["score"] for item in completeness_result]
    # for record in records:
    #     record["_completeness_score"] = scores[record.get("no") - 1]

    results = _evaluate_records(records)
    _print_summary(results)
    _write_csv(results, Path(__file__).parent / "results" / "history_eval_results.csv")


if __name__ == "__main__":
    asyncio.run(main())
