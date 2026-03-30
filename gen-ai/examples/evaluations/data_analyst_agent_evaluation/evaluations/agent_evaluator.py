"""Agent evaluator for assessing data analyst agent performance.

Provides metrics for evaluating agent responses:
- metric_has_answer: Checks for non-empty response
- metric_completeness_score: LLM-based scoring (1-3 scale)
- metric_resolution_rate: Chart validation via custom assertions
"""

import asyncio
import concurrent.futures
import json
import logging
from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar

import pandas as pd
import requests

from metrics import ResolutionRateMetric, completeness_score
from utils import iter_messages, iter_tool_call_steps, load_dataframe

logger = logging.getLogger(__name__)
F = TypeVar("F", bound=Callable[..., Any])


def log_metric(func: F) -> F:
    """Decorator to log metric method execution and results."""

    @wraps(func)
    def wrapper(self: "AgentEvaluator", record: dict[str, Any]) -> Any:
        try:
            result = func(self, record)
            logger.info("metric %s: %s", func.__name__, result)
            return result
        except Exception:
            logger.exception("metric %s raised an error", func.__name__)
            raise

    return wrapper  # type: ignore[return-value]


class AgentEvaluator:
    """Evaluates agent trajectory records using configurable metrics.

    Each metric method accepts a record and returns a value specific to that metric:
    - has_answer: Returns bool
    - completeness_score: Returns float (1-3 scale)
    - resolution_rate: Returns bool, requires assertion parameter
    """

    _logger = logger

    def __init__(self, query_id: int) -> None:
        self.query_id = query_id

    def _is_visualization_required(self, record: dict[str, Any]) -> bool:
        """Check if the record requires chart visualization.

        Args:
            record: Test case record dictionary.

        Returns:
            True if record requires visualization, False otherwise.
        """
        return record.get("requires_visualization", "FALSE") == "TRUE"

    def _is_generating_image(self, record: dict[str, Any]) -> bool:
        """Check if agent response claims to contain an image.

        Args:
            record: Test case record dictionary.

        Returns:
            True if answer contains '[image]' marker, False otherwise.
        """
        return "[image]" in record.get("answer", "")

    def _load_trajectory(self, record: dict[str, Any]) -> list[dict[str, Any]] | None:
        """Load agent trajectory from URL or JSON string.

        Args:
            record: Test case record dictionary with 'generated_agent_trajectory' field.

        Returns:
            List of trajectory messages, or None if loading fails.
        """
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
            logger.warning("JSON loading failed for trajectory")
            return None

    def _extract_generation_steps(
        self, record: dict[str, Any], agent_name: str, tool_name: str
    ) -> list[Any] | None:
        """Extract tool call steps from trajectory matching agent and tool.

        Args:
            record: Test case record dictionary.
            agent_name: Name of the agent to filter by.
            tool_name: Name of the tool to filter by.

        Returns:
            List of matching tool call steps, or None if no trajectory found.
        """
        messages = self._load_trajectory(record)
        if not messages:
            logger.info("No trajectory found")
            return None
        flat = list(iter_messages(messages))
        return list(iter_tool_call_steps(flat, agent=agent_name, tool_name=tool_name))

    def _check_no_generation_steps(self, record: dict[str, Any]) -> bool | None:
        """Determine resolution when no generation steps exist.

        Args:
            record: Test case record dictionary.

        Returns:
            True: If visualization not required.
            False: If claims image but didn't generate.
            None: Fall through to default failure.
        """
        if self._is_generating_image(record):
            logger.info("Claims to have image, but fails to generate one")
            return False
        if not self._is_visualization_required(record):
            logger.info("Visualization not required, missing generation step is OK")
            return True
        logger.info("No generation agent step found")
        return None

    def _evaluate_resolution_steps(
        self, steps: list[Any], assertion: Callable[[str, dict], bool]
    ) -> bool:
        """Evaluate resolution steps in reverse order, return True on first success.

        Args:
            steps: List of generation step objects from trajectory.
            assertion: Callable that validates chart output (code, namespace) -> bool.

        Returns:
            True if any step passes the assertion, False otherwise.
        """
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
    def metric_has_answer(self, record: dict[str, Any]) -> bool:
        """Check if record contains a non-empty answer.

        Args:
            record: Test case record dictionary.

        Returns:
            True if answer field is non-empty after stripping whitespace.
        """
        return bool(record.get("answer", "").strip())

    @log_metric
    def metric_completeness_score(self, record: dict[str, Any]) -> float:
        """Calculate LLM-based completeness score (scale 1-3).

        Uses external LLM to judge answer quality against expected answer.

        Args:
            record: Test case record with 'query', 'answer', 'expected_answer' fields.

        Returns:
            Completeness score as float between 1.0 and 3.0.
        """
        query = record.get("query", "")
        response = record.get("answer", "")
        expected = record.get("expected_answer", "")

        def _run_completeness() -> float:
            with asyncio.Runner() as runner:
                return runner.run(
                    completeness_score(
                        {
                            "query": query,
                            "answer": response,
                            "expected_answer": expected,
                        }
                    )
                )

        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            return executor.submit(_run_completeness).result()

    @log_metric
    def metric_resolution_rate(
        self, record: dict[str, Any], assertion: Callable[[str, dict], bool]
    ) -> bool:
        """Validate chart code execution against provided assertion.

        Args:
            record: Test case record containing trajectory
            assertion: Callable(code: str, namespace: dict) -> bool
                      Validates chart output

        Returns:
            True if any generation step passes the assertion
        """
        steps = self._extract_generation_steps(
            record, "graph_generation_agent", "python_repl"
        )
        if steps is None:
            return False
        if not steps:
            result = self._check_no_generation_steps(record)
            return result if result is not None else False
        return self._evaluate_resolution_steps(steps, assertion)
