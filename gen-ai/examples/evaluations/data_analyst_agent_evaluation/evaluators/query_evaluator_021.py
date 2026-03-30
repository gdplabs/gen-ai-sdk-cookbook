"""Evaluator for query ID 21: Price per share of OmniHoldingsMZV comparison from latest and previous round."""

from utils import check_currency_value_in_string, iter_messages
from .base import BaseQueryEvaluator, log_metric

_TARGET_COMPANY = "OmniHoldingsMZV"
_EXPECTED_LATEST_PPS = "$6,886,246"
_EXPECTED_PREVIOUS_PPS = "$7,584,183"


class QueryEvaluator021(BaseQueryEvaluator):
    """Evaluator for query ID 21.

    Query: What was the price per share of OmniHoldingsMZV during its latest recorded
    investment round compared to its previous rounds?

    Expected: Latest Round (Seed, 18th December 2017): $6,886,246 per share;
    Previous Round (Seed, 31st August 2017): $7,584,183 per share. PPS decreased.

    Metrics applied per HIGH_ALIGNMENT_METRIC_GUIDE.MD:

    Base class (inherited):
        - metric_has_answer       — non-empty answer (#2 Task Success proxy)
        - metric_keyword_match    — required keywords present (pps values + decrease)

    Custom (this class):
        - metric_trajectory_has_final_answer    — #2 Task Success: pipeline produced a response
        - metric_sql_targeted_correct_entity    — #13 Tool Calling Correctness / #15 SQL Correctness:
                                                SQL query targeted 'OmniHoldingsMZV'
        - metric_answer_grounded_in_tool_output — #11 Faithfulness: expected numeric values appeared
                                                in a tool result before the final answer was given
    """

    QUERY_ID = 21

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

        Verifies that the expected PPS values (6886246 and 7584183) appear in at least
        one tool result message within the trajectory, confirming the answer is grounded
        in retrieved data rather than hallucinated.
        """
        messages = self._load_trajectory(record)
        if not messages:
            return False

        for msg in iter_messages(messages):
            if msg.get("role") == "tool":
                content = msg.get("content", "")

                expected_latest_pps_in_content = check_currency_value_in_string(_EXPECTED_LATEST_PPS, content)
                expected_previous_pps_in_content = check_currency_value_in_string(_EXPECTED_PREVIOUS_PPS, content)
                if expected_latest_pps_in_content and expected_previous_pps_in_content:
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
