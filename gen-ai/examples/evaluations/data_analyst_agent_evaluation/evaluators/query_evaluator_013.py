"""Evaluator for query ID 13: AlphaSystemsL9K price per share comparison across rounds."""

from utils import check_currency_value_in_string, iter_messages
from .base import BaseQueryEvaluator, log_metric

_TARGET_COMPANY = "AlphaSystemsL9K"
# Latest and previous PPS values that must be grounded in tool output
_EXPECTED_LATEST_PPS = "8,267,114"
_EXPECTED_PREVIOUS_PPS = "3,458,972"
_SQL_TOOL_NAMES = {"data_checker", "sql_database_query"}


class QueryEvaluator013(BaseQueryEvaluator):
    """Evaluator for query ID 13.

    Query: How does the latest price per share for AlphaSystemsL9K compare to its previous round?

    Expected: Latest PPS $8,267,114 (Feb 23, 2021) vs previous PPS $3,458,972 (Feb 15, 2020),
    an increase of ~139%.

    Metrics applied per HIGH_ALIGNMENT_METRIC_GUIDE.MD:

    Base class (inherited):
        - metric_has_answer       — non-empty answer (#2 Task Success proxy)
        - metric_keyword_match    — required keywords present (latest + price per share +
                                    both PPS values + previous + increase)

    Custom (this class):
        - metric_trajectory_has_final_answer    — #2 Task Success: pipeline produced a response
        - metric_sql_targeted_correct_entity    — #13 Tool Calling Correctness / #15 SQL Correctness:
                                                SQL query targeted 'AlphaSystemsL9K'
        - metric_answer_grounded_in_tool_output — #11 Faithfulness: both PPS values (latest and
                                                previous) appeared in tool results, confirming the
                                                comparison is grounded in retrieved data
    """

    QUERY_ID = 13

    @log_metric
    def metric_sql_targeted_correct_entity(self, record: dict) -> bool:
        """#13 Tool Calling Correctness / #15 SQL Correctness (deterministic proxy).

        Verifies that at least one SQL tool call in the trajectory targeted 'AlphaSystemsL9K'.
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

        Verifies that both the latest PPS (8267114) and the previous PPS (3458972) appear
        in at least one tool result message within the trajectory. Both values must be
        present to confirm the comparison is grounded in retrieved data rather than
        hallucinated.
        """
        messages = self._load_trajectory(record)
        if not messages:
            return False

        for msg in iter_messages(messages):
            if msg.get("role") == "tool":
                content = msg.get("content", "")
                expected_latest_in_content = check_currency_value_in_string(_EXPECTED_LATEST_PPS, content)
                expected_previous_in_content = check_currency_value_in_string(_EXPECTED_PREVIOUS_PPS, content)
                if expected_latest_in_content and expected_previous_in_content:
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
