"""Evaluator for query ID 17: OmniHoldingsMZV valuation changes over multiple investment rounds."""

from utils import check_currency_value_in_string, iter_messages
from .base import BaseQueryEvaluator, log_metric

_TARGET_COMPANY = "OmniHoldingsMZV"
# Pre-money valuations for all three rounds (used as grounding anchors)
_EXPECTED_PRE_MONEY = ["19,421,425,981", "53,417,769,309", "37,193,628,551"]
_EXPECTED_CURRENT = ["25,308,196,228", "58,387,776,273", "40,943,157,880"]


class QueryEvaluator017(BaseQueryEvaluator):
    """Evaluator for query ID 17.

    Query: How has OmniHoldingsMZV's valuation changed over multiple investment rounds?

    Expected: A table covering three Seed rounds (2016-12-15, 2017-08-31, 2017-12-18)
    with their respective pre-money and current valuations.

    Metrics applied per HIGH_ALIGNMENT_METRIC_GUIDE.MD:

    Base class (inherited):
        - metric_has_answer       — non-empty answer (#2 Task Success proxy)
        - metric_keyword_match    — required keywords present (all dates + all six figures)

    Custom (this class):
        - metric_trajectory_has_final_answer    — #2 Task Success: pipeline produced a response
        - metric_sql_targeted_correct_entity    — #13 Tool Calling Correctness / #15 SQL Correctness:
                                                  SQL query targeted 'OmniHoldingsMZV'
        - metric_answer_grounded_in_tool_output — #11 Faithfulness: all three pre-money valuation
                                                  figures appeared in a tool result, confirming the
                                                  multi-round data was retrieved, not hallucinated
    """

    QUERY_ID = 17

    @log_metric
    def metric_sql_targeted_correct_entity(self, record: dict) -> bool:
        """#13 Tool Calling Correctness / #15 SQL Correctness (deterministic proxy).

        Verifies that at least one data_checker tool call in the trajectory contained
        a SQL query targeting 'OmniHoldingsMZV'. Confirms the agent queried the right entity.
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

        Verifies that all three expected pre-money valuation figures appear in tool result
        messages within the trajectory, confirming the full multi-round history was retrieved
        from the database rather than hallucinated.
        """
        messages = self._load_trajectory(record)
        if not messages:
            return False

        # Collect all tool result content
        tool_content = ""
        for msg in iter_messages(messages):
            if msg.get("role") == "tool":
                tool_content += msg.get("content", "")

        return all(check_currency_value_in_string(value, tool_content) for value in _EXPECTED_PRE_MONEY)

    def get_enabled_metrics(self) -> list[str]:
        """Returns the list of enabled metrics for this evaluator.

        Returns:
            list[str]: List of metric names to be evaluated
        """
        return super().get_enabled_metrics() + [
            "metric_sql_targeted_correct_entity",
            "metric_answer_grounded_in_tool_output",
        ]

    def _get_resolution_assertion(self):
        def assert_no_curly_braces(code: str, namespace: dict) -> bool:
            fig = namespace["__fig__"]
            for ax in fig.axes:
                for text in ax.texts:
                    label = text.get_text()
                    assert (
                        "{" not in label and "}" not in label
                    ), f"Bar label contains literal curly braces (double-brace f-string bug): {label!r}"
            return True

        return assert_no_curly_braces
