"""Evaluator for query ID 20: Highest price per share company at latest investment round."""

from utils import check_currency_value_in_string, iter_messages
from .base import BaseQueryEvaluator, log_metric

_TARGET_COMPANY = "BetaGlobalVWS"
_EXPECTED_PPS = "$8,984,554"
_EXPECTED_CURRENT_VALUATION = "$11,477,182,067"


class QueryEvaluator020(BaseQueryEvaluator):
    """Evaluator for query ID 20.

    Query: Which company had the highest price per share at the time of its latest investment
    round, and how does it compare to its current valuation?

    Expected: BetaGlobalVWS with PPS of $8,984,554 and current valuation of $11,477,182,067.

    Metrics applied per HIGH_ALIGNMENT_METRIC_GUIDE.MD:

    Base class (inherited):
        - metric_has_answer       — non-empty answer (#2 Task Success proxy)
        - metric_keyword_match    — required keywords present (entity + PPS + current valuation)

    Custom (this class):
        - metric_trajectory_has_final_answer — #2 Task Success: pipeline produced a response
        - metric_sql_queries_pps_per_company — #13 Tool Calling Correctness / #15 SQL Correctness:
                                               a data_checker call retrieved the pps column,
                                               confirming the agent queried the right metric
        - metric_answer_grounded_in_tool_output — #11 Faithfulness: both the expected PPS (8984554)
                                                  and current valuation (11477182067) appeared in
                                                  tool results, confirming the answer is not hallucinated
    """

    QUERY_ID = 20

    @log_metric
    def metric_sql_queries_pps_per_company(self, record: dict) -> bool:
        """#13 Tool Calling Correctness / #15 SQL Correctness (deterministic proxy).

        Verifies that at least one data_checker tool call in the trajectory retrieved the
        pps (price per share) column, confirming the agent used the correct field to
        determine the highest price per share across companies.
        """
        messages = self._load_trajectory(record)
        if not messages:
            return False

        for msg in iter_messages(messages):
            for tc in msg.get("tool_calls", []):
                fn = tc.get("function", {})
                if fn.get("name") == "data_checker":
                    args = fn.get("arguments", "")
                    if "pps" in args:
                        return True
        return False

    @log_metric
    def metric_answer_grounded_in_tool_output(self, record: dict) -> bool:
        """#11 Faithfulness (deterministic proxy).

        Verifies that both the expected PPS (8984554) and current valuation (11477182067)
        appear in tool result messages within the trajectory, confirming the answer is
        grounded in retrieved data rather than hallucinated.
        """
        messages = self._load_trajectory(record)
        if not messages:
            return False

        tool_content = ""
        for msg in iter_messages(messages):
            if msg.get("role") == "tool":
                tool_content += msg.get("content", "")

        expected_pps_in_content = check_currency_value_in_string(_EXPECTED_PPS, tool_content)
        expected_current_valuation_in_content = check_currency_value_in_string(
            _EXPECTED_CURRENT_VALUATION, tool_content
        )
        return expected_pps_in_content and expected_current_valuation_in_content

    def get_enabled_metrics(self) -> list[str]:
        """Returns the list of enabled metrics for this evaluator.

        Returns:
            list[str]: List of metric names to be evaluated
        """
        return super().get_enabled_metrics() + [
            "metric_sql_queries_pps_per_company",
            "metric_answer_grounded_in_tool_output",
        ]
