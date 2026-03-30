"""Base class for query evaluators."""

import asyncio
import concurrent.futures
import json
import logging
from abc import ABC
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


class BaseQueryEvaluator(ABC):
    """Base class for query evaluators.

    Each evaluator should define:
    - QUERY_ID: int
    - metric_* methods that return bool
    """

    _logger = logger

    QUERY_ID: int
    VERDICT_METRICS = ["metric_completeness_score", "metric_resolution_rate"]

    def _is_visualization_required(self, record: dict) -> bool:
        return record.get("requires_visualization", "FALSE") == "TRUE"

    def _is_generating_image(self, record: dict) -> bool:
        """Check if the query requires generating an image."""
        return "[image]" in record.get("answer")

    def evaluate(self, record: dict) -> tuple[str, dict[str, bool]]:
        """Evaluate a single record.

        Args:
            record: Dictionary containing the record to evaluate

        Returns:
            Tuple of ("good" | "bad", {metric_name: result}) where verdict is
            "good" if all metrics pass, "bad" otherwise.
        """
        logger.critical(f"Evaluating no: {record['no']}")
        metrics = self._run_metrics(record)
        verdict = self._get_verdict(metrics)
        logger.info(f"Verdict: {verdict}")
        logger.info(f"Expected verdict: {record['manual_rr']}")
        return verdict, metrics

    def _get_verdict(self, metrics: dict[str, bool]) -> str:
        """Determine verdict based on metrics."""
        verdict_metrics = {k: v for k, v in metrics.items() if k in self.VERDICT_METRICS}
        return "good" if verdict_metrics and all(verdict_metrics.values()) else "bad"

    def _extract_generation_steps(self, record: dict, agent_name: str, tool_name: str) -> list | None:
        """Load trajectory and return graph_generation_agent python_repl tool call steps.

        Returns None if the trajectory cannot be loaded, or a (possibly empty) list of steps.
        """
        messages = self._load_trajectory(record)
        if not messages:
            logger.info("No trajectory found")
            return None

        flat = list(iter_messages(messages))
        return list(iter_tool_call_steps(flat, agent=agent_name, tool_name=tool_name))

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

    def _run_metrics(self, record: dict) -> dict[str, bool]:
        return {name: getattr(self, name)(record) for name in self.get_enabled_metrics()}

    @log_metric
    def metric_has_answer(self, record: dict) -> bool:
        """Check if the record has an answer."""
        return bool(record.get("answer", "").strip())

    @log_metric
    def metric_completeness_score(self, record: dict) -> bool:
        """#17 Completeness: LLM-based completeness score >= 3 (scale 1-3).

        Uses a pre-computed score injected by the runner (_completeness_score key)
        when available, avoiding a redundant LLM call. Falls back to a single
        synchronous call when running outside the batch runner.
        """
        passing_score = 3.0

        if "_completeness_score" in record:
            return record["_completeness_score"] >= passing_score

        # Fallback: compute individually (slow path, used outside batch runner)
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

    def _get_resolution_assertion(self) -> Callable:
        """Return the assertion callable used by metric_resolution_rate.

        Override in subclasses to change chart-type validation logic.
        """

        def assert_bar_chart_and_no_curly_braces(code: str, namespace: dict) -> bool:
            fig = namespace["__fig__"]
            for ax in fig.axes:
                assert len(ax.patches) > 0, "Chart has no bar patches — expected a bar chart"
                for text in ax.texts:
                    label = text.get_text()
                    assert (
                        "{" not in label and "}" not in label
                    ), f"Bar label contains literal curly braces (double-brace f-string bug): {label!r}"
            return True

        return assert_bar_chart_and_no_curly_braces

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

    @log_metric
    def metric_resolution_rate(self, record: dict) -> bool:
        """#3 Resolution Rate: chart passes the assertion and bar labels use correct f-string syntax.

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

    def get_enabled_metrics(self) -> list[str]:
        """Return the list of metric method names to run for this evaluator.

        Override in subclasses to control which metrics are executed.
        By default runs all methods prefixed with 'metric_'.
        """
        return ["metric_has_answer", "metric_completeness_score", "metric_resolution_rate"]
