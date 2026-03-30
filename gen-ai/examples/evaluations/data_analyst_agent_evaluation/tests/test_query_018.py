"""Evaluation tests for query 18."""

import json

import pytest

from evaluators import QueryEvaluator018


class TestQuery018:
    QUERY_ID = 18

    def test_evaluate(self, record, result_collector):
        evaluator = QueryEvaluator018()
        predicted, metrics = evaluator.evaluate(record)
        expected = "good" if record["manual_rr"] == "good" else "bad"
        failed_metrics = {name: result for name, result in metrics.items() if not result}

        result_collector.add(
            no=record["no"],
            query_id=self.QUERY_ID,
            predicted=predicted,
            expected=expected,
            match=(predicted == expected),
            manual_rr=record["manual_rr"],
            failed=json.dumps(failed_metrics),
        )

        assert predicted == expected, (
            f"Record {record['no']}: predicted={predicted}, expected={expected}, failed={failed_metrics}"
        )
