"""Evaluator for query ID 3: Initial valuation and price per share of FirmSolutionsT69."""

from metrics import SqlCorrectnessMetric
from utils import check_currency_value_in_string, iter_messages
from .base import BaseQueryEvaluator, log_metric

_TARGET_COMPANY = "FirmSolutionsT69"
_EXPECTED_VALUATION = "51,182,210,058"
_EXPECTED_PPS = "8,696,513"


class QueryEvaluator003(BaseQueryEvaluator):
    """Evaluator for query ID 3.

    Query: What was the valuation and price per share of FirmSolutionsT69 when we invested
    the first time?

    Expected: First investment on August 8, 2016 — Pre-money valuation of $51,182,210,058
    and price per share of $8,696,513.

    Metrics applied per HIGH_ALIGNMENT_METRIC_GUIDE.MD:

    Base class (inherited):
        - metric_has_answer       — non-empty answer (#2 Task Success proxy)
        - metric_keyword_match    — required keywords present (date + figures + entity)

    Custom (this class):
        - metric_trajectory_has_final_answer    — #2 Task Success: pipeline produced a response
        - metric_sql_targeted_correct_entity    — #13 Tool Calling Correctness / #15 SQL Correctness:
                                                SQL query targeted 'FirmSolutionsT69'
        - metric_answer_grounded_in_tool_output — #11 Faithfulness: expected numeric values appeared
                                                in a tool result before the final answer was given
        - metric_completeness_score             — #17 Completeness: LLM-based score >= 2 (scale 1-3)
    """

    QUERY_ID = 3

    @log_metric
    def metric_sql_targeted_correct_entity(self, record: dict) -> bool:
        """#13 Tool Calling Correctness / #15 SQL Correctness (deterministic proxy).

        Verifies that at least one data_checker tool call in the trajectory contained
        a SQL query targeting 'FirmSolutionsT69'.
        Confirms the agent called the right tool with the right parameters.
        """
        messages = self._load_trajectory(record)
        if not messages:
            return False

        for msg in iter_messages(messages):
            for tc in msg.get("tool_calls", []):
                fn = tc.get("function", {})
                if fn.get("name") == "data_checker":
                    args = fn.get("arguments", "")
                    if _TARGET_COMPANY in args:
                        return True
        return False

    @log_metric
    def metric_answer_grounded_in_tool_output(self, record: dict) -> bool:
        """#11 Faithfulness (deterministic proxy).

        Verifies that the expected numeric values (51182210058 and 8696513) appear
        in at least one tool result message within the trajectory, confirming the
        answer is grounded in retrieved data rather than hallucinated.
        """
        messages = self._load_trajectory(record)
        if not messages:
            return False

        for msg in iter_messages(messages):
            if msg.get("role") == "tool":
                content = msg.get("content", "")
                valuation_in_content = check_currency_value_in_string(_EXPECTED_VALUATION, content)
                pps_in_content = check_currency_value_in_string(_EXPECTED_PPS, content)
                if valuation_in_content and pps_in_content:
                    return True
        return False

    @log_metric
    def metric_sql_correctness(self, record: dict) -> bool:
        """#18 SQL Correctness: SQL query correctly answers the user's question.

        Uses the SqlCorrectnessMetric to evaluate if the SQL query in the trajectory
        correctly answers the user's question.
        """
        return (
            SqlCorrectnessMetric().score(
                user_question=record.get("query", ""),
                trajectory=self._load_trajectory(record) or [],
            )
            >= 1.0
        )

    def get_enabled_metrics(self) -> list[str]:
        """Returns the list of enabled metrics for this evaluator.

        Returns:
            list[str]: List of metric names to be evaluated
        """
        return super().get_enabled_metrics() + [
            "metric_sql_targeted_correct_entity",
            "metric_answer_grounded_in_tool_output",
            "metric_sql_correctness",
        ]
