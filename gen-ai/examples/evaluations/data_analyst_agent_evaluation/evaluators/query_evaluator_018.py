"""Evaluator for query ID 18: Top three sectors by total investment across all geographies."""

from utils import check_currency_value_in_string, iter_messages
from .base import BaseQueryEvaluator, log_metric

# Top-3 sector totals (aggregated across all currencies/geographies)
_EXPECTED_TOP_SECTORS = ["Entertainment", "Fund", "Technology"]
_EXPECTED_TOTALS = ["741,973,010", "658,961,238", "567,839,169"]


class QueryEvaluator018(BaseQueryEvaluator):
    """Evaluator for query ID 18.

    Query: What are the top three sectors receiving the highest investment across all geographies?

    Expected: Entertainment ($741,973,010), Fund ($658,961,238), Technology ($567,839,169).

    Metrics applied per HIGH_ALIGNMENT_METRIC_GUIDE.MD:

    Base class (inherited):
        - metric_has_answer       — non-empty answer (#2 Task Success proxy)
        - metric_keyword_match    — required keywords present (sector names + figure prefixes)

    Custom (this class):
        - metric_trajectory_has_final_answer    — #2 Task Success: pipeline produced a response
        - metric_sql_fetches_sector_investments — #13 Tool Calling Correctness / #15 SQL Correctness:
                                                  a data_checker call retrieved category and
                                                  commited_value from the investments table
        - metric_answer_grounded_in_tool_output — #11 Faithfulness: all three expected sector totals
                                                  appeared in tool results, confirming the ranking
                                                  is grounded in retrieved data
    """

    QUERY_ID = 18

    @log_metric
    def metric_sql_fetches_sector_investments(self, record: dict) -> bool:
        """#13 Tool Calling Correctness / #15 SQL Correctness (deterministic proxy).

        Verifies that at least one data_checker tool call in the trajectory retrieved
        both the category (sector) and commited_value columns from the investments table.
        Confirms the agent queried the right table and columns to answer the question.
        """
        messages = self._load_trajectory(record)
        if not messages:
            return False

        for msg in iter_messages(messages):
            for tc in msg.get("tool_calls", []):
                fn = tc.get("function", {})
                if fn.get("name") == "data_checker":
                    args = fn.get("arguments", "")
                    if "category" in args and "commited_value" in args:
                        return True
        return False

    @log_metric
    def metric_answer_grounded_in_tool_output(self, record: dict) -> bool:
        """#11 Faithfulness (deterministic proxy).

        Verifies that all three expected sector totals (741,973,010, 658,961,238, 567,839,169)
        appear in tool result messages within the trajectory, confirming the top-3 ranking
        is grounded in retrieved data rather than hallucinated.
        """
        messages = self._load_trajectory(record)
        if not messages:
            return False

        tool_content = ""
        for msg in iter_messages(messages):
            if msg.get("role") == "tool":
                tool_content += msg.get("content", "")

        return all(check_currency_value_in_string(total, tool_content) for total in _EXPECTED_TOTALS)

    def get_enabled_metrics(self) -> list[str]:
        """Returns the list of enabled metrics for this evaluator.

        Returns:
            list[str]: List of metric names to be evaluated
        """
        return super().get_enabled_metrics() + [
            "metric_sql_fetches_sector_investments",
            "metric_answer_grounded_in_tool_output",
        ]
