"""Evaluator for query ID 12: Price per share for OmniIndustries5B8's most recent investment round."""

from utils import check_currency_value_in_string, iter_messages
from .base import BaseQueryEvaluator, log_metric

_TARGET_COMPANY = "OmniIndustries5B8"
# Expected PPS value from the most recent (Secondary) round
_EXPECTED_PPS = "5,283,255"
# SQL tool names that may appear in different trajectory variants
_SQL_TOOL_NAMES = {"data_checker", "sql_database_query"}


class QueryEvaluator012(BaseQueryEvaluator):
    """Evaluator for query ID 12.

    Query: What was the price per share for OmniIndustries5B8 during its most recent
    investment round?

    Expected: $5,283,255 — Secondary round on June 26, 2022.

    Metrics applied per HIGH_ALIGNMENT_METRIC_GUIDE.MD:

    Base class (inherited):
        - metric_has_answer       — non-empty answer (#2 Task Success proxy)
        - metric_keyword_match    — required keywords present (price per share + entity + date + $5)

    Custom (this class):
        - metric_trajectory_has_final_answer    — #2 Task Success: pipeline produced a response
        - metric_sql_targeted_correct_entity    — #13 Tool Calling Correctness / #15 SQL Correctness:
                                                SQL query targeted 'OmniIndustries5B8'
        - metric_answer_grounded_in_tool_output — #11 Faithfulness: expected PPS value appeared
                                                in tool results before the final answer was given
    """

    QUERY_ID = 12

    @log_metric
    def metric_sql_targeted_correct_entity(self, record: dict) -> bool:
        """#13 Tool Calling Correctness / #15 SQL Correctness (deterministic proxy).

        Verifies that at least one SQL tool call in the trajectory contained a query
        targeting 'OmniIndustries5B8'.
        """
        messages = self._load_trajectory(record)
        if not messages:
            return False

        for msg in iter_messages(messages):
            for tc in msg.get("tool_calls", []):
                fn = tc.get("function", {})
                if fn.get("name") in _SQL_TOOL_NAMES:
                    args = fn.get("arguments", "")
                    if _TARGET_COMPANY in args:
                        return True
        return False

    @log_metric
    def metric_answer_grounded_in_tool_output(self, record: dict) -> bool:
        """#11 Faithfulness (deterministic proxy).

        Verifies that the expected PPS value (5283255) appears in at least one tool
        result message within the trajectory, confirming the answer is grounded in
        retrieved data rather than hallucinated.
        """
        messages = self._load_trajectory(record)
        if not messages:
            return False

        for msg in iter_messages(messages):
            if msg.get("role") == "tool":
                content = msg.get("content", "")
                if check_currency_value_in_string(_EXPECTED_PPS, content):
                    return True
        return False

    def get_enabled_metrics(self) -> list[str]:
        """Returns the list of enabled metrics for this evaluator.

        Returns:
            list[str]: List of metric names to be evaluated
        """
        return super().get_enabled_metrics() + [
            "metric_sql_targeted_correct_entity",
            "metric_answer_grounded_in_tool_output",
        ]
