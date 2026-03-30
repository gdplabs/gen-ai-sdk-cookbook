"""Evaluator for query ID 11: Total committed capital for OmniIndustries5B8 across Series B and C."""

from utils import check_currency_value_in_string, iter_messages
from .base import BaseQueryEvaluator, log_metric

_TARGET_COMPANY = "OmniIndustries5B8"
_REQUIRED_ROUNDS = ("Series B", "Series C")
# Raw committed values returned by the SQL tool
_EXPECTED_RAW_VALUE_1 = "26,762,267"
_EXPECTED_RAW_VALUE_2 = "14,196,215"
_EXPECTED_RAW_VALUE_3 = "69,640,428"
# SQL tool names that may appear in different trajectory variants
_SQL_TOOL_NAMES = {"data_checker", "sql_database_query"}


class QueryEvaluator011(BaseQueryEvaluator):
    """Evaluator for query ID 11.

    Query: What is the total committed capital for OmniIndustries5B8 across all
    Series B and Series C rounds?

    Expected: $110,598,910 total across Series B and Series C rounds.

    Metrics applied per HIGH_ALIGNMENT_METRIC_GUIDE.MD:

    Base class (inherited):
        - metric_has_answer       — non-empty answer (#2 Task Success proxy)
        - metric_keyword_match    — required keywords present (total + entity + rounds + $110)

    Custom (this class):
        - metric_trajectory_has_final_answer    — #2 Task Success: pipeline produced a response
        - metric_sql_targeted_correct_entity    — #13 Tool Calling Correctness / #15 SQL Correctness:
                                                SQL query targeted 'OmniIndustries5B8'
        - metric_sql_filtered_by_round          — #15 SQL Correctness: SQL filtered by Series B/C rounds
        - metric_answer_grounded_in_tool_output — #11 Faithfulness: expected raw DB values appeared
                                                in tool results before the final answer was given
    """

    QUERY_ID = 11

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
    def metric_sql_filtered_by_round(self, record: dict) -> bool:
        """#15 SQL Correctness: SQL must filter by both Series B and Series C.

        Verifies that at least one SQL tool call in the trajectory contained both
        'Series B' and 'Series C' in its arguments, confirming the agent correctly
        scoped the query to the requested investment rounds.
        """
        messages = self._load_trajectory(record)
        if not messages:
            return False

        for msg in iter_messages(messages):
            for tc in msg.get("tool_calls", []):
                fn = tc.get("function", {})
                if fn.get("name") in _SQL_TOOL_NAMES:
                    args = fn.get("arguments", "")
                    if all(r in args for r in _REQUIRED_ROUNDS):
                        return True
        return False

    @log_metric
    def metric_answer_grounded_in_tool_output(self, record: dict) -> bool:
        """#11 Faithfulness (deterministic proxy).

        Verifies that the raw committed values (26762267 and 14196215) appear in at
        least one tool result message within the trajectory, confirming the answer
        is grounded in retrieved data rather than hallucinated.
        """
        messages = self._load_trajectory(record)
        if not messages:
            return False

        for msg in iter_messages(messages):
            if msg.get("role") == "tool":
                content = msg.get("content", "")
                expected_1_in_content = check_currency_value_in_string(_EXPECTED_RAW_VALUE_1, content)
                expected_2_in_content = check_currency_value_in_string(_EXPECTED_RAW_VALUE_2, content)
                expected_3_in_content = check_currency_value_in_string(_EXPECTED_RAW_VALUE_3, content)
                if expected_1_in_content and expected_2_in_content and expected_3_in_content:
                    return True
        return False

    def get_enabled_metrics(self) -> list[str]:
        """Returns the list of enabled metrics for this evaluator.

        Returns:
            list[str]: List of metric names to be evaluated
        """
        return super().get_enabled_metrics() + [
            "metric_sql_targeted_correct_entity",
            "metric_sql_filtered_by_round",
            "metric_answer_grounded_in_tool_output",
        ]
