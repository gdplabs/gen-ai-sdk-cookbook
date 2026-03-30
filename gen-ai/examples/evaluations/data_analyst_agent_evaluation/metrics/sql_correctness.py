"""SQL correctness metric.

Author:
    - Mikhael Chris (mikhael.chris@gdplabs.id)
"""

import asyncio
import concurrent.futures
import json
import logging
import os

from deepeval.test_case import LLMTestCaseParams
from dotenv import load_dotenv
from gllm_evals.metrics.deepeval_geval import DeepEvalGEvalMetric
from gllm_evals.types import RAGData

from utils import iter_messages

logger = logging.getLogger(__name__)


class SqlCorrectnessMetric:
    """LLM-as-a-Judge metric that determines whether the SQL in a trajectory correctly answers the user's question.

    Usage::

        metric = SqlCorrectnessMetric()
        result: bool = metric.score(user_question, trajectory)
    """

    _SQL_TOOL_NAMES = {"data_checker", "sql_database_query"}

    def score(self, user_question: str, trajectory: list) -> float:
        """Return True if the SQL query in the trajectory correctly answers the user's question.

        Args:
            user_question: The user's question to evaluate the SQL against.
            trajectory: List of message dicts from the agent trajectory.

        Returns:
            float: Score (0-1) where 1 means SQL correctly answers the question, 0 means it doesn't.
        """
        if not user_question or not user_question.strip():
            logger.warning("SqlCorrectnessMetric: user_question is empty.")
            return 0

        sql_queries = self._extract_sql_queries(trajectory)
        if not sql_queries:
            logger.warning("SqlCorrectnessMetric: no SQL queries found in trajectory.")
            return 0

        sql_query = "\n\n".join(sql_queries)

        def _run():
            with asyncio.Runner() as runner:
                return runner.run(self._evaluate(user_question, sql_query))

        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
            return pool.submit(_run).result()

    async def _evaluate(self, user_question: str, sql_query: str) -> float:
        """LLM-judge whether `sql_query` correctly answers `user_question`."""
        load_dotenv()

        metric = DeepEvalGEvalMetric(
            name="SQL Correctness",
            evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
            criteria=(
                "Determine whether the SQL query correctly answers the user's question. "
                "A correct SQL query must: target the right entities/tables, apply "
                "appropriate filters matching the user's constraints, and return the "
                "data (columns/aggregations) needed to answer the question."
            ),
            evaluation_steps=[
                "Identify the key entities, filters, and data requested in the user's question.",
                "Check whether the SQL query targets the correct entities and columns.",
                "Verify that the SQL query's WHERE clauses and conditions match the user's constraints.",
                "Confirm that any aggregations (GROUP BY, SUM, COUNT, etc.) align with what the user asked.",
                "Score 1 (correct) if all elements align, 0 (incorrect) if any critical element is wrong.",
            ],
            model_credentials=os.getenv("GOOGLE_API_KEY"),
            threshold=0.5,
        )

        try:
            logger.critical(user_question)
            logger.critical(sql_query)
            result = await metric.evaluate(
                RAGData(
                    query=user_question,
                    generated_response=sql_query,
                )
            )
            logger.info(f"SQL correctness score for '{user_question[:50]}...': {result}")
            return float(result.get("score", 0))
        except Exception as e:
            logger.warning(f"SqlCorrectnessMetric: failed to evaluate: {e}. Returning False.")
            return -1

    def _parse_sql(self, tc: dict) -> str | None:
        """Extract SQL string from a tool call dict, or None if not a SQL tool call."""
        fn = tc.get("function", {})
        if fn.get("name") not in self._SQL_TOOL_NAMES:
            return None
        args_raw = fn.get("arguments", "")
        try:
            args = json.loads(args_raw) if isinstance(args_raw, str) else args_raw
            query = args.get("query") or args.get("sql") or args_raw
        except (json.JSONDecodeError, AttributeError):
            query = args_raw
        return str(query) if query else None

    def _extract_sql_queries(self, messages: list) -> list[str]:
        """Return the last SQL query string found in tool calls across the trajectory."""
        for msg in reversed(list(iter_messages(messages))):
            for tc in reversed(msg.get("tool_calls", [])):
                query = self._parse_sql(tc)
                if query:
                    return [query]
        return []
