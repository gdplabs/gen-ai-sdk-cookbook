"""Evaluator for query ID 22: Pie chart of committed investment in AI category across countries."""

import json

from utils import iter_messages
from .base import BaseQueryEvaluator, log_metric

_TARGET_CATEGORY = "AI"
# Countries expected in the tool output
_EXPECTED_COUNTRIES = ["GERMANY", "KOREA", "SOUTH KOREA", "UK", "USA"]


class QueryEvaluator022(BaseQueryEvaluator):
    """Evaluator for query ID 22.

    Query: Show a pie chart of committed investment in the AI category across different countries.

    Expected: A pie chart showing UK dominates, South Korea is a strong contender, USA holds a
    moderate share, and Germany/Korea have the lowest shares.

    Metrics applied per HIGH_ALIGNMENT_METRIC_GUIDE.MD:

    Base class (inherited):
        - metric_has_answer       — non-empty answer (#2 Task Success proxy)
        - metric_keyword_match    — required keywords present (country insight phrases)

    Custom (this class):
        - metric_trajectory_has_final_answer    — #2 Task Success: pipeline produced a response
        - metric_sql_filtered_by_ai_category    — #13 Tool Calling Correctness / #15 SQL Correctness:
                                                SQL filtered by category = 'AI' and grouped by country
        - metric_graph_generation_called        — #13 Tool Calling Correctness: graph generation
                                                agent was delegated to for the pie chart
        - metric_answer_grounded_in_tool_output — #11 Faithfulness: all expected countries appeared
                                                in tool results before the final answer
    """

    QUERY_ID = 22

    @log_metric
    def metric_sql_filtered_by_ai_category(self, record: dict) -> bool:
        """#13 Tool Calling Correctness / #15 SQL Correctness (deterministic proxy).

        Verifies that at least one data_checker tool call used a SQL query filtering by
        category = 'AI' and grouping by country.
        """
        messages = self._load_trajectory(record)
        if not messages:
            return False

        for msg in iter_messages(messages):
            for tc in msg.get("tool_calls", []):
                fn = tc.get("function", {})
                if fn.get("name") == "data_checker":
                    args = fn.get("arguments", "")
                    if _TARGET_CATEGORY in args and "country" in args.lower():
                        return True
        return False

    @log_metric
    def metric_graph_generation_called(self, record: dict) -> bool:
        """#13 Tool Calling Correctness (deterministic proxy).

        Verifies that the graph generation agent was delegated to, confirming the agent
        attempted to produce the requested pie chart visualization.
        """
        messages = self._load_trajectory(record)
        if not messages:
            return False

        for msg in iter_messages(messages):
            for tc in msg.get("tool_calls", []):
                fn = tc.get("function", {})
                if "graph_generation" in fn.get("name", ""):
                    return True
                # Also accept python_repl with return_plot flag
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

        Verifies that all expected country names appeared in tool result messages within
        the trajectory, confirming the answer is grounded in retrieved data.
        """
        messages = self._load_trajectory(record)
        if not messages:
            return False

        tool_content = ""
        for msg in iter_messages(messages):
            if msg.get("role") == "tool":
                tool_content += msg.get("content", "")

        return all(country in tool_content for country in _EXPECTED_COUNTRIES)

    def get_enabled_metrics(self) -> list[str]:
        """Returns the list of enabled metrics for this evaluator.

        Returns:
            list[str]: List of metric names to be evaluated
        """
        return super().get_enabled_metrics() + [
            "metric_sql_filtered_by_ai_category",
            "metric_graph_generation_called",
            "metric_answer_grounded_in_tool_output",
        ]
