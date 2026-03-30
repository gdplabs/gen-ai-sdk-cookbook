"""Evaluator for query ID 15: Highest total investment year in the Technology sector."""

from utils import check_currency_value_in_string, iter_messages
from .base import BaseQueryEvaluator, log_metric

_TECHNOLOGY_CATEGORY = "Technology"
_EXPECTED_YEAR = "2018"
_EXPECTED_TOTAL = "218716888"


class QueryEvaluator015(BaseQueryEvaluator):
    """Evaluator for query ID 15.

    Query: Which year saw the highest total investment in the Technology sector?

    Expected: 2018 with a total investment of $218,716,888 (≈ $218.7 million).

    Metrics applied per HIGH_ALIGNMENT_METRIC_GUIDE.MD:

    Base class (inherited):
        - metric_has_answer       — non-empty answer (#2 Task Success proxy)
        - metric_keyword_match    — required keywords present (year + superlative + figure)

    Custom (this class):
        - metric_trajectory_has_final_answer    — #2 Task Success: pipeline produced a response
        - metric_sql_filters_technology_category — #13 Tool Calling Correctness / #15 SQL Correctness:
                                                  SQL query filtered on the Technology category
        - metric_answer_grounded_in_tool_output — #11 Faithfulness: expected year and total value
                                                  appeared in a tool result before the final answer
    """

    QUERY_ID = 15

    @log_metric
    def metric_sql_filters_technology_category(self, record: dict) -> bool:
        """#13 Tool Calling Correctness / #15 SQL Correctness (deterministic proxy).

        Verifies that at least one data_checker tool call in the trajectory contained
        a SQL query filtering on the 'Technology' category.
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
                    if _TECHNOLOGY_CATEGORY in args:
                        return True
        return False

    @log_metric
    def metric_answer_grounded_in_tool_output(self, record: dict) -> bool:
        """#11 Faithfulness (deterministic proxy).

        Verifies that the expected year (2018) and aggregated total (218716888)
        appear in at least one tool result message within the trajectory, confirming
        the answer is grounded in retrieved data rather than hallucinated.
        """
        messages = self._load_trajectory(record)
        if not messages:
            return False

        for msg in iter_messages(messages):
            if msg.get("role") == "tool":
                content = msg.get("content", "")
                expected_year_in_content = _EXPECTED_YEAR in content
                expected_total_in_content = check_currency_value_in_string(_EXPECTED_TOTAL, content)
                if expected_year_in_content and expected_total_in_content:
                    return True
        return False

    def get_enabled_metrics(self) -> list[str]:
        """Returns the list of enabled metrics for this evaluator.

        Returns:
            list[str]: List of metric names to be evaluated
        """
        return super().get_enabled_metrics() + [
            "metric_sql_filters_technology_category",
            "metric_answer_grounded_in_tool_output",
        ]
