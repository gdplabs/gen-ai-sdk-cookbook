"""Agent evaluator for data analyst agent evaluation."""

import asyncio
import concurrent.futures
import json
import logging
from collections.abc import Callable
from functools import wraps

import pandas as pd
import requests

from metrics import ResolutionRateMetric, completeness_score
from utils import iter_messages, iter_tool_call_steps, load_dataframe

logger = logging.getLogger(__name__)


def log_metric(func):
    """Decorator to log the result of a metric method."""

    @wraps(func)
    def wrapper(self, record):
        try:
            result = func(self, record)
            logger.info("metric %s: %s", func.__name__, result)
            return result
        except Exception:
            logger.exception("metric %s raised an error", func.__name__)
            raise

    return wrapper


# ---------------------------------------------------------------------------
# Resolution assertion functions
# ---------------------------------------------------------------------------


def _assert_bar_chart_and_no_curly_braces(code: str, namespace: dict) -> bool:
    fig = namespace["__fig__"]
    for ax in fig.axes:
        assert len(ax.patches) > 0, "Chart has no bar patches — expected a bar chart"
        for text in ax.texts:
            label = text.get_text()
            assert (
                "{" not in label and "}" not in label
            ), f"Bar label contains literal curly braces (double-brace f-string bug): {label!r}"
    return True


def _assert_no_curly_braces_only(code: str, namespace: dict) -> bool:
    fig = namespace["__fig__"]
    for ax in fig.axes:
        for text in ax.texts:
            label = text.get_text()
            assert (
                "{" not in label and "}" not in label
            ), f"Bar label contains literal curly braces (double-brace f-string bug): {label!r}"
    return True


def _assert_line_chart_and_no_curly_braces(code: str, namespace: dict) -> bool:
    fig = namespace["__fig__"]
    for ax in fig.axes:
        assert len(ax.lines) > 0, "Chart has no lines — expected a line chart"
        for text in ax.texts:
            label = text.get_text()
            assert (
                "{" not in label and "}" not in label
            ), f"Text contains literal curly braces (double-brace f-string bug): {label!r}"
    return True


_RESOLUTION_ASSERTIONS: dict[int, Callable] = {
    17: _assert_no_curly_braces_only,
    23: _assert_line_chart_and_no_curly_braces,
}


class AgentEvaluator:
    """Evaluates a single pre-recorded agent trajectory record.

    Runs three metrics:
    - metric_has_answer: non-empty answer
    - metric_completeness_score: LLM-based completeness >= 3 (scale 1-3)
    - metric_resolution_rate: generated chart code passes assertion

    Verdict is "good" if completeness_score and resolution_rate both pass.
    """

    _logger = logger

    def __init__(self, query_id: int):
        self.query_id = query_id

    def evaluate(self, record: dict) -> tuple[str, dict[str, bool]]:
        """Evaluate a single record.

        Returns:
            Tuple of ("good" | "bad", {metric_name: result}).
        """
        logger.critical(f"Evaluating no: {record['no']}")
        metrics = {
            "metric_has_answer": self.metric_has_answer(record),
            "metric_completeness_score": self.metric_completeness_score(record),
            "metric_resolution_rate": self.metric_resolution_rate(record),
        }
        verdict = "good" if metrics["metric_completeness_score"] and metrics["metric_resolution_rate"] else "bad"
        logger.info(f"Verdict: {verdict}")
        logger.info(f"Expected verdict: {record['manual_rr']}")
        return verdict, metrics

    def _is_visualization_required(self, record: dict) -> bool:
        return record.get("requires_visualization", "FALSE") == "TRUE"

    def _is_generating_image(self, record: dict) -> bool:
        return "[image]" in record.get("answer")

    def _load_trajectory(self, record: dict) -> list | None:
        raw = record.get("generated_agent_trajectory", "")
        if not raw:
            return None
        if isinstance(raw, str) and raw.startswith("http"):
            try:
                response = requests.get(raw, timeout=30)
                response.raise_for_status()
                return response.json()
            except Exception:
                logger.exception("Failed to fetch trajectory from URL: %s", raw)
                return None
        try:
            return json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            logger.warning("JSON loading failed")
            return None

    def _extract_generation_steps(self, record: dict, agent_name: str, tool_name: str) -> list | None:
        """Load trajectory and return tool call steps filtered by agent and tool name."""
        messages = self._load_trajectory(record)
        if not messages:
            logger.info("No trajectory found")
            return None

        flat = list(iter_messages(messages))
        return list(iter_tool_call_steps(flat, agent=agent_name, tool_name=tool_name))

    def _check_no_generation_steps(self, record: dict) -> bool | None:
        """Determine resolution result when no generation steps are found.

        Returns True/False for an early exit, or None to fall through to False.
        """
        if self._is_generating_image(record):
            logger.info("Claims to have image, but fails to generate one")
            return False
        if not self._is_visualization_required(record):
            logger.info("Visualization is not required, therefore not having generation agent step is okay")
            return True
        logger.info("No generation agent step found")
        return None

    def _evaluate_resolution_steps(self, steps: list, assertion: Callable) -> bool:
        """Iterate steps in reverse and return True on the first successful assertion."""
        for step in reversed(steps):
            args = json.loads(step.arguments)
            sql_query = args.get("sql_query")
            code = args.get("code")
            if not code:
                continue
            df = pd.DataFrame([])
            if sql_query:
                df = load_dataframe(sql_query)
            if ResolutionRateMetric().evaluate(code=code, assertion=assertion, df=df):
                return True

        logger.info("No step produced a valid chart")
        return False

    def _get_resolution_assertion(self) -> Callable:
        return _RESOLUTION_ASSERTIONS.get(self.query_id, _assert_bar_chart_and_no_curly_braces)

    @log_metric
    def metric_has_answer(self, record: dict) -> bool:
        """Check if the record has a non-empty answer."""
        return bool(record.get("answer", "").strip())

    @log_metric
    def metric_completeness_score(self, record: dict) -> bool:
        """LLM-based completeness score >= 3 (scale 1-3)."""
        passing_score = 3.0
        query, response, expected_response = (
            record.get("query", ""),
            record.get("answer", ""),
            record.get("expected_answer", ""),
        )

        def _run():
            with asyncio.Runner() as runner:
                return runner.run(
                    completeness_score({"query": query, "answer": response, "expected_answer": expected_response})
                )

        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            return executor.submit(_run).result() >= passing_score

    @log_metric
    def metric_resolution_rate(self, record: dict) -> bool:
        """Chart passes the assertion and bar labels use correct f-string syntax.

        Executes the generated graph code with real data from the database, then verifies
        the chart via the assertion returned by _get_resolution_assertion().
        """
        steps = self._extract_generation_steps(record, "graph_generation_agent", "python_repl")
        if steps is None:
            return False
        if not steps:
            result = self._check_no_generation_steps(record)
            return result if result is not None else False
        return self._evaluate_resolution_steps(steps, self._get_resolution_assertion())
