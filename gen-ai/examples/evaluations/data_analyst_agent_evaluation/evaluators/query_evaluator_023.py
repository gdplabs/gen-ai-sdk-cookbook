"""Evaluator for query ID 23: Line chart of trend committed capital for NexusIndustries82V over time."""

import json

from utils import check_currency_value_in_string, iter_messages
from .base import BaseQueryEvaluator, log_metric

_TARGET_COMPANY = "NexusIndustries82V"
# Committed capital values expected in tool output across the three investment dates
_EXPECTED_VALUES = ["$76,565,120", "$37,779,424", "$12,236,805"]


class QueryEvaluator023(BaseQueryEvaluator):
    """Evaluator for query ID 23.

    Query: Show a line chart of the trend in committed capital for NexusIndustries82V over time.

    Expected: Line chart showing committed capital peaked in 2016 ($76.57M), dropped to $37.78M
    in 2017, and further declined to $12.24M by 2020.

    Metrics applied per HIGH_ALIGNMENT_METRIC_GUIDE.MD:

    Base class (inherited):
        - metric_has_answer       — non-empty answer (#2 Task Success proxy)
        - metric_keyword_match    — required keywords present (trend insight phrases)

    Custom (this class):
        - metric_trajectory_has_final_answer    — #2 Task Success: pipeline produced a response
        - metric_sql_targeted_correct_entity    — #13 Tool Calling Correctness / #15 SQL Correctness:
                                                SQL query targeted 'NexusIndustries82V'
        - metric_graph_generation_called        — #13 Tool Calling Correctness: graph generation
                                                agent was delegated to for the line chart
        - metric_answer_grounded_in_tool_output — #11 Faithfulness: expected committed capital values
                                                appeared in tool results before the final answer
    """

    QUERY_ID = 23

    @log_metric
    def metric_sql_targeted_correct_entity(self, record: dict) -> bool:
        """#13 Tool Calling Correctness / #15 SQL Correctness (deterministic proxy).

        Verifies that at least one data_checker tool call in the trajectory contained
        a SQL query targeting 'NexusIndustries82V'.
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
    def metric_graph_generation_called(self, record: dict) -> bool:
        """#13 Tool Calling Correctness (deterministic proxy).

        Verifies that the graph generation agent was delegated to, confirming the agent
        attempted to produce the requested line chart visualization.
        """
        messages = self._load_trajectory(record)
        if not messages:
            return False

        for msg in iter_messages(messages):
            for tc in msg.get("tool_calls", []):
                fn = tc.get("function", {})
                if "graph_generation" in fn.get("name", ""):
                    return True
                if fn.get("name") == "python_repl":
                    args_str = fn.get("arguments", "")
                    try:
                        args = json.loads(args_str) if isinstance(args_str, str) else args_str
                        if args.get("return_plot") is True:
                            return True
                    except (json.JSONDecodeError, AttributeError):
                        if '"return_plot": true' in args_str:
                            return True
        return False

    @log_metric
    def metric_answer_grounded_in_tool_output(self, record: dict) -> bool:
        """#11 Faithfulness (deterministic proxy).

        Verifies that all three expected committed capital values appeared in tool result
        messages within the trajectory, confirming the answer is grounded in retrieved data.
        """
        messages = self._load_trajectory(record)
        if not messages:
            return False

        tool_content = ""
        for msg in iter_messages(messages):
            if msg.get("role") == "tool":
                tool_content += msg.get("content", "")

        return all(check_currency_value_in_string(value, tool_content) for value in _EXPECTED_VALUES)

    def get_enabled_metrics(self) -> list[str]:
        """Returns the list of enabled metrics for this evaluator.

        Returns:
            list[str]: List of metric names to be evaluated
        """
        return super().get_enabled_metrics() + [
            "metric_sql_targeted_correct_entity",
            "metric_graph_generation_called",
            "metric_answer_grounded_in_tool_output",
        ]

    def _get_resolution_assertion(self):
        def assert_line_chart_and_no_curly_braces(code: str, namespace: dict) -> bool:
            fig = namespace["__fig__"]
            for ax in fig.axes:
                assert len(ax.lines) > 0, "Chart has no lines — expected a line chart"
                for text in ax.texts:
                    label = text.get_text()
                    assert (
                        "{" not in label and "}" not in label
                    ), f"Text contains literal curly braces (double-brace f-string bug): {label!r}"
            return True

        return assert_line_chart_and_no_curly_braces
