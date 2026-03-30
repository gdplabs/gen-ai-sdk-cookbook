"""Evaluator for query ID 1: BizGroupYPZ valuation and price per share in May 2016."""

from utils import check_currency_value_in_string, iter_messages
from .base import BaseQueryEvaluator, log_metric

_EXPECTED_VALUATION = "70,286,218,717"
_EXPECTED_PPS = "1,122,051"
_TARGET_COMPANY = "BizGroupYPZ"
_TARGET_DATE_PREFIX = "2016-05"


class QueryEvaluator001(BaseQueryEvaluator):
    """Evaluator for query ID 1.

    Query: What was BizGroupYPZ's valuation and price per share in May 2016?

    Expected: Pre-money valuation of $70,286,218,717 and price per share of $1,122,051.

    Metrics applied per HIGH_ALIGNMENT_METRIC_GUIDE.MD:

    Base class (inherited):
        - metric_has_answer       — non-empty answer (#2 Task Success proxy)
        - metric_keyword_match    — required keywords present (exact figures + entity)

    Custom (this class):
        - metric_trajectory_has_final_answer    — #2 Task Success: pipeline produced a response
        - metric_sql_targeted_correct_entity    — #13 Tool Calling Correctness / #15 SQL Correctness:
                                                SQL query targeted 'BizGroupYPZ' in May 2016
        - metric_answer_grounded_in_tool_output — #11 Faithfulness: expected numeric values appeared
                                                in a tool result before the final answer was given
    """

    QUERY_ID = 1

    @log_metric
    def metric_sql_targeted_correct_entity(self, record: dict) -> bool:
        """#13 Tool Calling Correctness / #15 SQL Correctness (deterministic proxy).

        Verifies that at least one data_checker tool call in the trajectory contained
        a SQL query targeting 'BizGroupYPZ' with a May 2016 date filter.
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
                    if _TARGET_COMPANY in args and _TARGET_DATE_PREFIX in args:
                        return True
        return False

    @log_metric
    def metric_answer_grounded_in_tool_output(self, record: dict) -> bool:
        """#11 Faithfulness (deterministic proxy).

        Verifies that the expected numeric values ($70,286,218,717 and $1,122,051) appear
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

    def get_enabled_metrics(self) -> list[str]:
        """Return the list of metric method names to run for this evaluator.

        Override in subclasses to control which metrics are executed.
        By default runs all methods prefixed with 'metric_'.
        """
        return super().get_enabled_metrics() + [
            "metric_sql_targeted_correct_entity",
            "metric_answer_grounded_in_tool_output",
        ]
