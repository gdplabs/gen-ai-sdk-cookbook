"""Evaluator for query ID 14: Capital committed each year for investments in the UK."""

from utils import check_currency_value_in_string, iter_messages
from .base import BaseQueryEvaluator, log_metric

# Expected per-year totals that must appear in tool output
_EXPECTED_2016 = "118,445,462"
_EXPECTED_2017 = "254,486,317"
_EXPECTED_2018 = "135,433,896"
_EXPECTED_2019 = "43,218,585"
_EXPECTED_2020 = "12,236,805"
_SQL_TOOL_NAMES = {"data_checker", "sql_database_query"}


class QueryEvaluator014(BaseQueryEvaluator):
    """Evaluator for query ID 14.

    Query: How much capital has been committed each year for investments in the UK?

    Expected:
    Here is the analysis of the total capital committed each year for investments in the UK:

    ### Table
    | Year | Total Committed   |
    |------|-------------------|
    | 2016 | 118,445,462.0     |
    | 2017 | 254,486,317.0     |
    | 2018 | 135,433,896.0     |
    | 2019 | 43,218,585.0      |
    | 2020 | 12,236,805.0      |

    ### Visualization


    ### Key Insights
    - **Total Committed Capital**: The highest amount was committed in 2017, with a total of 254,486,317.0.
    - **Trend**: There is a noticeable decline in committed capital from 2017 to 2020.



    Metrics applied per HIGH_ALIGNMENT_METRIC_GUIDE.MD:

    Base class (inherited):
        - metric_has_answer       — non-empty answer (#2 Task Success proxy)
        - metric_keyword_match    — required keywords present (each year, UK, all 5 year values,
                                    highest)

    Custom (this class):
        - metric_trajectory_has_final_answer    — #2 Task Success: pipeline produced a response
        - metric_sql_filtered_by_country_uk     — #15 SQL Correctness: SQL filtered by country = 'UK'
        - metric_sql_grouped_by_year            — #15 SQL Correctness: SQL used GROUP BY to aggregate
                                                per year rather than returning raw rows
        - metric_answer_grounded_in_tool_output — #11 Faithfulness: expected per-year totals appeared
                                                in tool results before the final answer was given
    """

    QUERY_ID = 14

    @log_metric
    def metric_sql_filtered_by_country_uk(self, record: dict) -> bool:
        """#15 SQL Correctness: SQL must scope the query to UK investments.

        Verifies that at least one SQL tool call in the trajectory filtered by
        country = 'UK', confirming the agent did not return global investment data.
        """
        messages = self._load_trajectory(record)
        if not messages:
            return False

        for msg in iter_messages(messages):
            for tc in msg.get("tool_calls", []):
                fn = tc.get("function", {})
                if fn.get("name") in _SQL_TOOL_NAMES:
                    args = fn.get("arguments", "")
                    if "'UK'" in args or '"UK"' in args:
                        return True
        return False

    @log_metric
    def metric_answer_grounded_in_tool_output(self, record: dict) -> bool:
        """#11 Faithfulness (deterministic proxy).

        Verifies that the 2016 total (118445462) and 2017 total (254486317) both appear
        in at least one tool result message, confirming the per-year breakdown is grounded
        in retrieved data rather than hallucinated.
        """
        messages = self._load_trajectory(record)
        if not messages:
            return False

        for msg in iter_messages(messages):
            if msg.get("role") == "tool":
                content = msg.get("content", "")
                expected_2016_in_content = check_currency_value_in_string(
                    _EXPECTED_2016, content
                )
                expected_2017_in_content = check_currency_value_in_string(
                    _EXPECTED_2017, content
                )
                expected_2018_in_content = check_currency_value_in_string(
                    _EXPECTED_2018, content
                )
                expected_2019_in_content = check_currency_value_in_string(
                    _EXPECTED_2019, content
                )
                expected_2020_in_content = check_currency_value_in_string(
                    _EXPECTED_2020, content
                )
                if (
                    expected_2016_in_content
                    and expected_2017_in_content
                    and expected_2018_in_content
                    and expected_2019_in_content
                    and expected_2020_in_content
                ):
                    return True
        return False

    def get_enabled_metrics(self) -> list[str]:
        """Returns the list of enabled metrics for this evaluator.

        Returns:
            list[str]: List of metric names to be evaluated
        """
        return super().get_enabled_metrics() + [
            "metric_sql_filtered_by_country_uk",
            "metric_answer_grounded_in_tool_output",
        ]
