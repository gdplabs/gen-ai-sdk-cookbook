"""Evaluator for query ID 19: Entertainment sector investments by country with chart."""

from utils import check_currency_value_in_string, iter_messages
from .base import BaseQueryEvaluator, log_metric

_ENTERTAINMENT_CATEGORY = "Entertainment"
# Country totals present in raw data_checker results (as float substrings)
_GROUNDING_VALUES = ["597,783,513", "75,198,601", "61,045,022", "7,105,565", "840,309"]


class QueryEvaluator019(BaseQueryEvaluator):
    """Evaluator for query ID 19.

    Query: How do investments in the entertainment sector vary across different countries?
    Please provide a chart for visualization.

    Expected: Country breakdown (USA $597,783,513 · RUSSIA $75,198,601 · UK $61,045,022 ·
    CHINA $7,105,565 · INDONESIA $840,309) plus a generated chart.

    Metrics applied per HIGH_ALIGNMENT_METRIC_GUIDE.MD:

    Base class (inherited):
        - metric_has_answer       — non-empty answer (#2 Task Success proxy)
        - metric_keyword_match    — required keywords present (all five country totals)

    Custom (this class):
        - metric_trajectory_has_final_answer    — #2 Task Success: pipeline produced a response
        - metric_sql_filters_entertainment      — #13 Tool Calling Correctness / #15 SQL Correctness:
                                                  a data_checker call filtered on 'Entertainment'
        - metric_graph_generation_attempted     — #13 Tool Calling Correctness: a chart was requested
                                                  (python_repl called with return_plot or a graph
                                                  agent was delegated to)
        - metric_answer_grounded_in_tool_output — #11 Faithfulness: representative country-level
                                                  figures appeared in tool results, confirming
                                                  the breakdown is grounded in retrieved data
    """

    QUERY_ID = 19

    @log_metric
    def metric_sql_filters_entertainment(self, record: dict) -> bool:
        """#13 Tool Calling Correctness / #15 SQL Correctness (deterministic proxy).

        Verifies that at least one data_checker tool call in the trajectory filtered
        on the 'Entertainment' category. Confirms the agent queried the right sector.
        """
        messages = self._load_trajectory(record)
        if not messages:
            return False

        for msg in iter_messages(messages):
            for tc in msg.get("tool_calls", []):
                fn = tc.get("function", {})
                if fn.get("name") == "data_checker":
                    args = fn.get("arguments", "")
                    if _ENTERTAINMENT_CATEGORY in args:
                        return True
        return False

    @log_metric
    def metric_graph_generation_attempted(self, record: dict) -> bool:
        """#13 Tool Calling Correctness: chart generation was attempted.

        Verifies that either a graph_generation_agent was delegated to or a python_repl
        call included 'return_plot' in its arguments, confirming the agent tried to
        fulfill the visualization request.
        """
        messages = self._load_trajectory(record)
        if not messages:
            return False

        for msg in iter_messages(messages):
            for tc in msg.get("tool_calls", []):
                fn = tc.get("function", {})
                name = fn.get("name", "")
                args = fn.get("arguments", "")
                if "graph_generation" in name:
                    return True
                if name == "python_repl" and "return_plot" in args:
                    return True
        return False

    @log_metric
    def metric_answer_grounded_in_tool_output(self, record: dict) -> bool:
        """#11 Faithfulness (deterministic proxy).

        Verifies that representative country-level investment figures (Russia: 75198601,
        Indonesia: 840309, China: 7105565) appear in tool result messages within the
        trajectory, confirming the country breakdown is grounded in retrieved data.
        """
        messages = self._load_trajectory(record)
        if not messages:
            return False

        tool_content = ""
        for msg in iter_messages(messages):
            if msg.get("role") == "tool":
                tool_content += msg.get("content", "")

        return all(check_currency_value_in_string(value, tool_content) for value in _GROUNDING_VALUES)

    def get_enabled_metrics(self) -> list[str]:
        """Returns the list of enabled metrics for this evaluator.

        Returns:
            list[str]: List of metric names to be evaluated
        """
        return super().get_enabled_metrics() + [
            "metric_sql_filters_entertainment",
            "metric_graph_generation_attempted",
            "metric_answer_grounded_in_tool_output",
        ]
