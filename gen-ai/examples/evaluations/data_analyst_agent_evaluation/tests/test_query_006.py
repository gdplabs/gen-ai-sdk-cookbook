"""Evaluation tests for query 6."""

import json

import pytest

from evaluators import QueryEvaluator006


class TestQuery006:
    QUERY_ID = 6

    def test_evaluate(self, record, result_collector):
        evaluator = QueryEvaluator006()
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
