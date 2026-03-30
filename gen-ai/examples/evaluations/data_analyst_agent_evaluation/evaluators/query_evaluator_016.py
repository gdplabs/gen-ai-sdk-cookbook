"""Evaluator for query ID 16: Pre-money vs current valuation comparison for OmniIndustries5B8."""

from utils import check_currency_value_in_string, iter_messages
from .base import BaseQueryEvaluator, log_metric

_TARGET_COMPANY = "OmniIndustries5B8"
_EXPECTED_CURRENT_VALUATION = "11,973,878,195"
_EXPECTED_PRE_MONEY_VALUATION = "5,621,758,037"
_SQL_TOOL_NAMES = {"data_checker", "sql_database_query"}


class QueryEvaluator016(BaseQueryEvaluator):
    """Evaluator for query ID 16.

    Query: What is the latest current valuation of OmniIndustries5B8, and how does it
    compare to its pre-money valuation?

    Expected: Current valuation of $11,973,878,195 vs pre-money valuation of $5,621,758,037
    (≈ 2.13× increase).

    Metrics applied per HIGH_ALIGNMENT_METRIC_GUIDE.MD:

    Base class (inherited):
        - metric_has_answer       — non-empty answer (#2 Task Success proxy)
        - metric_keyword_match    — required keywords present (entity + both figures)

    Custom (this class):
        - metric_trajectory_has_final_answer    — #2 Task Success: pipeline produced a response
        - metric_sql_targeted_correct_entity    — #13 Tool Calling Correctness / #15 SQL Correctness:
                                                  SQL query targeted 'OmniIndustries5B8'
        - metric_answer_grounded_in_tool_output — #11 Faithfulness: both expected valuation figures
                                                  appeared in a tool result before the final answer
    """

    QUERY_ID = 16

    @log_metric
    def metric_sql_targeted_correct_entity(self, record: dict) -> bool:
        """#13 Tool Calling Correctness / #15 SQL Correctness (deterministic proxy).

        Verifies that at least one SQL tool call in the trajectory contained a query
        targeting 'OmniIndustries5B8'. Confirms the agent called the right tool with
        the right parameters.
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

        Verifies that both the current valuation (11973878195) and pre-money valuation
        (5621758037) appear in at least one tool result message within the trajectory,
        confirming the answer is grounded in retrieved data rather than hallucinated.
        """
        messages = self._load_trajectory(record)
        if not messages:
            return False

        for msg in iter_messages(messages):
            if msg.get("role") == "tool":
                content = msg.get("content", "")
                expected_current_valuation_in_content = check_currency_value_in_string(
                    _EXPECTED_CURRENT_VALUATION, content
                )
                expected_pre_money_valuation_in_content = check_currency_value_in_string(
                    _EXPECTED_PRE_MONEY_VALUATION, content
                )
                if expected_current_valuation_in_content and expected_pre_money_valuation_in_content:
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
