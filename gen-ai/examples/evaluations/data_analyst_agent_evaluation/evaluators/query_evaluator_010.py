"""Evaluator for query ID 10: Capital committed to OmniHoldingsMZV."""

from utils import check_currency_value_in_string, iter_messages
from .base import BaseQueryEvaluator, log_metric

_TARGET_COMPANY = "OmniHoldingsMZV"
# Raw committed values returned by the SQL tool
_EXPECTED_RAW_VALUE_1 = "2,455,369"
_EXPECTED_RAW_VALUE_2 = "41,854,893"
_EXPECTED_RAW_VALUE_3 = "77,438,283"
# Summed result produced by the pandas agent
_EXPECTED_SUM = "121,748,545"


class QueryEvaluator010(BaseQueryEvaluator):
    """Evaluator for query ID 10.

    Query: How much capital has been committed to OmniHoldingsMZV?

    Expected: Total committed capital of $121,748,545 (keyword prefix $121).

    Metrics applied per HIGH_ALIGNMENT_METRIC_GUIDE.MD:

    Base class (inherited):
        - metric_has_answer       — non-empty answer (#2 Task Success proxy)
        - metric_keyword_match    — required keywords present (total + entity + $121)

    Custom (this class):
        - metric_trajectory_has_final_answer    — #2 Task Success: pipeline produced a response
        - metric_sql_targeted_correct_entity    — #13 Tool Calling Correctness / #15 SQL Correctness:
                                                SQL query targeted 'OmniHoldingsMZV'
        - metric_answer_grounded_in_tool_output — #11 Faithfulness: expected raw DB values appeared
                                                in tool results before the final answer was given
    """

    QUERY_ID = 10

    @log_metric
    def metric_sql_targeted_correct_entity(self, record: dict) -> bool:
        """#13 Tool Calling Correctness / #15 SQL Correctness (deterministic proxy).

        Verifies that at least one data_checker tool call in the trajectory contained
        a SQL query targeting 'OmniHoldingsMZV'.
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
                    if _TARGET_COMPANY in args:
                        return True
        return False

    @log_metric
    def metric_answer_grounded_in_tool_output(self, record: dict) -> bool:
        """#11 Faithfulness (deterministic proxy).

        Verifies that the raw committed values (2455369 and 41854893) appear in at
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
            "metric_answer_grounded_in_tool_output",
        ]
