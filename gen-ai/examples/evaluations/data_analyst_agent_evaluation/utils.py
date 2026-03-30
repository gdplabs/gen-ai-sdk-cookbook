"""Shared utility helpers for evaluation."""

import re
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
import sqlalchemy


@dataclass
class ToolCallStep:
    """A single tool call paired with its response."""

    tool_call_id: str
    function_name: str
    arguments: str
    response_content: str
    agent: str


def iter_tool_call_steps(
    messages: list[dict],
    *,
    agent: str | None = None,
    tool_name: str | None = None,
) -> Iterator[ToolCallStep]:
    """Yield ToolCallStep objects from a flattened (iterated) message list.

    Optionally filter by agent name and/or tool (function) name.
    """
    # Build response index: tool_call_id -> content
    response_index: dict[str, str] = {}
    for msg in messages:
        if msg.get("role") == "tool":
            tc_id = msg.get("tool_call_id", "")
            if tc_id:
                response_index[tc_id] = msg.get("content", "")

    # Yield steps from assistant messages with tool_calls
    for msg in messages:
        if msg.get("role") != "assistant":
            continue
        tool_calls = msg.get("tool_calls")
        if not tool_calls:
            continue

        msg_agent = msg.get("metadata", {}).get("agent", "")
        if agent is not None and agent not in msg_agent:
            continue

        for tc in tool_calls:
            fn = tc.get("function", {})
            fn_name = fn.get("name", "")
            if tool_name is not None and fn_name != tool_name:
                continue

            tc_id = tc.get("id", "")
            yield ToolCallStep(
                tool_call_id=tc_id,
                function_name=fn_name,
                arguments=fn.get("arguments", ""),
                response_content=response_index.get(tc_id, ""),
                agent=msg_agent,
            )


_DEFAULT_DB_PATH = Path(__file__).parent / "database.sqlite"
_DEFAULT_CONNECTION_STRING = f"sqlite:///{_DEFAULT_DB_PATH}"


def load_dataframe(
    query: str,
    connection_string: str = _DEFAULT_CONNECTION_STRING,
) -> pd.DataFrame:
    """Load a DataFrame by executing *query* against the given database.

    Args:
        query: SQL SELECT statement to execute.
        connection_string: SQLAlchemy connection URL.
            Defaults to the local ``database.sqlite`` file.

    Returns:
        pandas DataFrame with the query results.
    """
    engine = sqlalchemy.create_engine(connection_string)
    with engine.connect() as conn:
        return pd.read_sql_query(sqlalchemy.text(query), conn)


def iter_messages(messages: list):
    """Recursively yield every message including those in sub_trajectories."""
    for msg in messages:
        yield msg
        sub = msg.get("metadata", {}).get("sub_trajectory", [])
        if sub:
            yield from iter_messages(sub)


def check_currency_value_in_string(currency_value: str, text: str) -> bool:
    """Check if a currency value is present in a string."""
    cleaned_currency_value = re.sub(r"\D", "", currency_value)
    separated_with_space_currency_value = currency_value.replace(",", " ")
    return cleaned_currency_value in text or currency_value in text or separated_with_space_currency_value in text
