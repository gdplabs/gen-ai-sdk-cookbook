"""Evaluator for query ID 4: Comparison of capital committed in AI sector in 2016 vs 2019."""

from utils import check_currency_value_in_string, iter_messages
from .base import BaseQueryEvaluator, log_metric

_TARGET_CATEGORY = "AI"
_TARGET_YEAR_2016 = "2016"
_TARGET_YEAR_2019 = "2019"
_EXPECTED_2016 = "2,455,369"
_EXPECTED_2019 = "30,083,026"


class QueryEvaluator004(BaseQueryEvaluator):
    """Evaluator for query ID 4.

    Query: How much capital did we commit in the AI sector in 2016 compare to 2019?

    Expected: 2016 total $2,455,369 and 2019 total $30,083,026 in the AI sector,
    with a significant increase noted.

    Metrics applied per HIGH_ALIGNMENT_METRIC_GUIDE.MD:

    Base class (inherited):
        - metric_has_answer       — non-empty answer (#2 Task Success proxy)
        - metric_keyword_match    — required keywords present (years + figures + trend)

    Custom (this class):
        - metric_trajectory_has_final_answer    — #2 Task Success: pipeline produced a response
        - metric_sql_targeted_correct_entity    — #13 Tool Calling Correctness / #15 SQL Correctness:
                                                SQL query targeted 'AI' category with 2016 and 2019
        - metric_answer_grounded_in_tool_output — #11 Faithfulness: expected numeric values appeared
                                                in a tool result before the final answer was given
    """

    QUERY_ID = 4

    @log_metric
    def metric_sql_targeted_correct_entity(self, record: dict) -> bool:
        """#13 Tool Calling Correctness / #15 SQL Correctness (deterministic proxy).

        Verifies that at least one data_checker tool call in the trajectory contained
        a SQL query targeting the 'AI' category with both 2016 and 2019 year filters.
        Confirms the agent called the right tool with the right parameters.
        """
        messages = self._load_trajectory(record)
        if not messages:
            return False

        for msg in iter_messages(messages):
            for tc in msg.get("tool_calls", []):
                fn = tc.get("function", {})
                if fn.get("name") in ["data_checker", "sql_database_query"]:
                    args = fn.get("arguments", "")
                    if _TARGET_CATEGORY in args.upper() and _TARGET_YEAR_2016 in args and _TARGET_YEAR_2019 in args:
                        return True
        return False

    @log_metric
    def metric_answer_grounded_in_tool_output(self, record: dict) -> bool:
        """#11 Faithfulness (deterministic proxy).

        Verifies that the expected numeric values ($2,455,369 and $30,083,026) appear
        in at least one tool result message within the trajectory, confirming the
        answer is grounded in retrieved data rather than hallucinated.
        """
        messages = self._load_trajectory(record)
        if not messages:
            return False

        for msg in iter_messages(messages):
            if msg.get("role") == "tool":
                content = msg.get("content", "")
                expected_2016_exists = check_currency_value_in_string(_EXPECTED_2016, content)
                expected_2019_exists = check_currency_value_in_string(_EXPECTED_2019, content)
                if expected_2016_exists and expected_2019_exists:
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
