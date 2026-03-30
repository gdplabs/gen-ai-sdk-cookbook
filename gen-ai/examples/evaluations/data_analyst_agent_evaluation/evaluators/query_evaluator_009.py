"""Evaluator for query ID 9: Bar chart comparing total investment by year."""

from utils import check_currency_value_in_string, iter_messages
from .base import BaseQueryEvaluator, log_metric

# Raw value for 2022 — the year with the highest total investment
_EXPECTED_2015_RAW = "10,334,547"
_EXPECTED_2016_RAW = "158,593,985"
_EXPECTED_2017_RAW = "348,244,797"
_EXPECTED_2018_RAW = "706,734,337"
_EXPECTED_2019_RAW = "592,889,944"
_EXPECTED_2020_RAW = "224,444,205"
_EXPECTED_2021_RAW = "538,241,983"
_EXPECTED_2022_RAW = "790,311,598"


class QueryEvaluator009(BaseQueryEvaluator):
    """Evaluator for query ID 9.

    Query: Create a bar chart showing the year with the highest total investment and
    compare it to other years.

    Expected: 2022 is the highest investment year ($790,311,598 combined). The agent
    must produce a bar chart and a breakdown of investment totals per year (with
    per-currency detail in the final answer).

    Metrics applied per HIGH_ALIGNMENT_METRIC_GUIDE.MD:

    Base class (inherited):
        - metric_has_answer       — non-empty answer (#2 Task Success proxy)
        - metric_keyword_match    — required keywords present (years + figures)

    Custom (this class):
        - metric_trajectory_has_final_answer — #2 Task Success: pipeline produced a response
        - metric_sql_aggregates_by_year      — #13 Tool Calling Correctness / #15 SQL Correctness:
                                             SQL aggregated investments grouped by year
        - metric_answer_grounded_in_tool_output — #11 Faithfulness: expected raw values appeared
                                                in tool results before the final answer
        - metric_graph_generated             — #2 Task Success / output format: a plot image
                                             was produced by the graph generation agent
    """

    QUERY_ID = 9

    @log_metric
    def metric_sql_aggregates_by_year(self, record: dict) -> bool:
        """#13 Tool Calling Correctness / #15 SQL Correctness (deterministic proxy).

        Verifies that at least one data_checker tool call in the trajectory issued a
        SQL query that aggregates committed investment values grouped by year.
        Confirms the agent retrieved the right data shape for the bar chart.
        """
        messages = self._load_trajectory(record)
        if not messages:
            return False

        for msg in iter_messages(messages):
            for tc in msg.get("tool_calls", []):
                fn = tc.get("function", {})
                if fn.get("name") == "data_checker":
                    args = fn.get("arguments", "").lower()
                    if "commited_value" in args and "year" in args and "investment" in args:
                        return True
        return False

    @log_metric
    def metric_answer_grounded_in_tool_output(self, record: dict) -> bool:
        """#11 Faithfulness (deterministic proxy).

        Verifies that the raw 2018 and 2022 investment totals (706734337 and 790311598)
        appear in at least one tool result, confirming the chart data was retrieved from
        the database rather than hallucinated.
        """
        messages = self._load_trajectory(record)
        if not messages:
            return False

        for msg in iter_messages(messages):
            if msg.get("role") == "tool":
                content = msg.get("content", "")
                for expected_raw in [
                    _EXPECTED_2015_RAW,
                    _EXPECTED_2016_RAW,
                    _EXPECTED_2017_RAW,
                    _EXPECTED_2018_RAW,
                    _EXPECTED_2019_RAW,
                    _EXPECTED_2020_RAW,
                    _EXPECTED_2021_RAW,
                    _EXPECTED_2022_RAW,
                ]:
                    if not check_currency_value_in_string(expected_raw, content):
                        return False
                    return True
        return False

    @log_metric
    def metric_graph_generated(self, record: dict) -> bool:
        """#2 Task Success / output format (deterministic proxy).

        Verifies that a plot image was produced: at least one tool result in the
        trajectory references a generated PNG image, confirming the graph generation
        agent executed the visualization code with return_plot=true.
        """
        messages = self._load_trajectory(record)
        if not messages:
            return False

        for msg in iter_messages(messages):
            if msg.get("role") == "tool":
                content = msg.get("content", "")
                if ".png" in content and ("Generated Plot" in content or "![" in content):
                    return True
        return False

    def get_enabled_metrics(self) -> list[str]:
        """Returns the list of enabled metrics for this evaluator.

        Returns:
            list[str]: List of metric names to be evaluated
        """
        return super().get_enabled_metrics() + [
            "metric_sql_aggregates_by_year",
            "metric_answer_grounded_in_tool_output",
            "metric_graph_generated",
        ]
