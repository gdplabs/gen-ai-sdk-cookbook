"""Parametrized evaluation tests for the data analyst agent."""

import json

from evaluations.agent_evaluator import AgentEvaluator


def test_evaluate_agent(record, result_collector):
    """Evaluate a single pre-recorded agent trajectory.

    Validates that:
    - Agent produces a non-empty answer
    - Answer meets the completeness score threshold (LLM-judged, scale 1-3, pass >= 3)
    - Generated chart code executes successfully and passes chart assertion

    Verdict is "good" if completeness_score and resolution_rate both pass.
    """
    query_id = int(record["query_id"])
    evaluator = AgentEvaluator(query_id=query_id)

    predicted, metrics = evaluator.evaluate(record)
    expected = "good" if record["manual_rr"] == "good" else "bad"
    failed_metrics = {name: result for name, result in metrics.items() if not result}

    result_collector.add(
        no=record["no"],
        query_id=query_id,
        predicted=predicted,
        expected=expected,
        match=(predicted == expected),
        manual_rr=record["manual_rr"],
        failed=json.dumps(failed_metrics),
    )

    assert predicted == expected, (
        f"Record {record['no']}: predicted={predicted}, expected={expected}, failed={failed_metrics}"
    )
