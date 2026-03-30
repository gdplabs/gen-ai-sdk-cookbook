"""Evaluator for query ID 7: Capital committed in 2016."""

from utils import check_currency_value_in_string, iter_messages
from .base import BaseQueryEvaluator, log_metric

_TARGET_YEAR = "2016"
# EUR amount is a single raw DB row value — directly verifiable in tool results
_EXPECTED_USD_RAW = "144,480,885"
_EXPECTED_EUR_RAW = "14,113,100"


class QueryEvaluator007(BaseQueryEvaluator):
    """Evaluator for query ID 7.

    Query: How much capital have we committed in 2016?

    Expected: USD 144,480,885 and EUR 14,113,100 committed in 2016.

    Metrics applied per HIGH_ALIGNMENT_METRIC_GUIDE.MD:

    Base class (inherited):
        - metric_has_answer       — non-empty answer (#2 Task Success proxy)
        - metric_keyword_match    — required keywords present (year + USD amount + EUR amount)

    Custom (this class):
        - metric_trajectory_has_final_answer — #2 Task Success: pipeline produced a response
        - metric_sql_queried_year_2016       — #13 Tool Calling Correctness / #15 SQL Correctness:
                                             SQL filtered investments by year 2016
        - metric_answer_grounded_in_tool_output — #11 Faithfulness: EUR raw value (14113100)
                                                appeared in a tool result, confirming retrieval
                                                from the database rather than hallucination
    """

    QUERY_ID = 7

    @log_metric
    def metric_sql_queried_year_2016(self, record: dict) -> bool:
        """#13 Tool Calling Correctness / #15 SQL Correctness (deterministic proxy).

        Verifies that at least one data_checker tool call in the trajectory contained
        a SQL query filtering investments by year 2016.
        """
        messages = self._load_trajectory(record)
        if not messages:
            return False

        for msg in iter_messages(messages):
            for tc in msg.get("tool_calls", []):
                fn = tc.get("function", {})
                if fn.get("name") == "data_checker":
                    args = fn.get("arguments", "")
                    if _TARGET_YEAR in args and "investment" in args.lower():
                        return True
        return False

    @log_metric
    def metric_answer_grounded_in_tool_output(self, record: dict) -> bool:
        """#11 Faithfulness (deterministic proxy).

        Verifies that the EUR committed value (14113100) appears in at least one tool
        result message within the trajectory, confirming the answer is grounded in
        retrieved data rather than hallucinated.
        """
        messages = self._load_trajectory(record)
        if not messages:
            return False

        for msg in iter_messages(messages):
            if msg.get("role") == "tool":
                content = msg.get("content", "")
                self._logger.info(f"Content: {content}")
                usd_in_content = check_currency_value_in_string(_EXPECTED_USD_RAW, content.replace("\u202f", ""))
                eur_in_content = check_currency_value_in_string(_EXPECTED_EUR_RAW, content.replace("\u202f", ""))
                self._logger.info(f"USD raw value: {usd_in_content}")
                self._logger.info(f"EUR raw value: {eur_in_content}")
                if usd_in_content and eur_in_content:
                    return True
        return False

    def get_enabled_metrics(self) -> list[str]:
        """Returns the list of enabled metrics for this evaluator.

        Returns:
            list[str]: List of metric names to be evaluated
        """
        return super().get_enabled_metrics() + [
            "metric_sql_queried_year_2016",
            "metric_answer_grounded_in_tool_output",
        ]
