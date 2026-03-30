"""Evaluator for query ID 2: Capital committed in OmniIndustries5B8's Entertainment investments."""

from utils import check_currency_value_in_string, iter_messages
from .base import BaseQueryEvaluator, log_metric

_TARGET_COMPANY = "OmniIndustries5B8"
_TARGET_CATEGORY = "Entertainment"
_EXPECTED_TOTAL = "344,404,167"


class QueryEvaluator002(BaseQueryEvaluator):
    """Evaluator for query ID 2.

    Query: How much capital did we commit in OmniIndustries5B8's investments within the
    Entertainment sector?

    Expected: OmniIndustries5B8 committed a total of $344,404,167 in the Entertainment sector.

    Metrics applied per HIGH_ALIGNMENT_METRIC_GUIDE.MD:

    Base class (inherited):
        - metric_has_answer       — non-empty answer (#2 Task Success proxy)
        - metric_keyword_match    — required keywords present (entity + amount + sector)

    Custom (this class):
        - metric_trajectory_has_final_answer    — #2 Task Success: pipeline produced a response
        - metric_sql_targeted_correct_entity    — #13 Tool Calling Correctness / #15 SQL Correctness:
                                                SQL query targeted OmniIndustries5B8 in Entertainment
        - metric_answer_grounded_in_tool_output — #11 Faithfulness: expected numeric value appeared
                                                in a tool result before the final answer was given
    """

    QUERY_ID = 2

    @log_metric
    def metric_sql_targeted_correct_entity(self, record: dict) -> bool:
        """#13 Tool Calling Correctness / #15 SQL Correctness (deterministic proxy).

        Verifies that at least one data_checker tool call in the trajectory contained
        a SQL query targeting 'OmniIndustries5B8' with an 'Entertainment' category filter.
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
                    if _TARGET_COMPANY in args and _TARGET_CATEGORY in args:
                        return True
        return False

    @log_metric
    def metric_answer_grounded_in_tool_output(self, record: dict) -> bool:
        """#11 Faithfulness (deterministic proxy).

        Verifies that the expected numeric total ($344,404,167) appears in at least one
        tool result message within the trajectory, confirming the answer is grounded
        in retrieved data rather than hallucinated.
        """
        messages = self._load_trajectory(record)
        if not messages:
            return False

        for msg in iter_messages(messages):
            if msg.get("role") == "tool":
                content = msg.get("content", "")
                if check_currency_value_in_string(_EXPECTED_TOTAL, content):
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
