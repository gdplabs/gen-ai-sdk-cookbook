"""Evaluation tests for the data analyst agent.

Test structure:
- test_standard_case: Runs all quality metrics (has_answer, completeness, resolution)
  for all query IDs except 17 and 23 (which have specialized tests).
- test_resolution_query_17: Only resolution_rate with no-curly-braces assertion.
- test_resolution_query_23: Only resolution_rate with line-chart assertion.
"""

from evaluations.agent_evaluator import AgentEvaluator

# =============================================================================
# Test case filtering
# =============================================================================

# Query IDs that require specialized resolution assertions
SPECIALIZED_QUERY_IDS = {17, 23}

# Standard query IDs: 1-23 excluding specialized
STANDARD_QUERY_IDS = [qid for qid in range(1, 24) if qid not in SPECIALIZED_QUERY_IDS]


# =============================================================================
# Assertion functions (used by metric_resolution_rate)
# =============================================================================


def _assert_bar_chart_and_no_curly_braces(code: str, namespace: dict) -> bool:
    """Assert chart has bar patches and no literal curly braces in labels.

    This is the default assertion for standard test cases.

    Args:
        code: Generated Python code string (unused but required by interface).
        namespace: Execution namespace containing __fig__ matplotlib figure.

    Returns:
        True if assertion passes.

    Raises:
        AssertionError: If chart has no bars or labels contain curly braces.
    """
    fig = namespace["__fig__"]
    for ax in fig.axes:
        assert len(ax.patches) > 0, "Chart has no bar patches — expected a bar chart"
        for text in ax.texts:
            label = text.get_text()
            assert (
                "{" not in label and "}" not in label
            ), f"Bar label contains literal curly braces: {label!r}"
    return True


def _assert_no_curly_braces_only(code: str, namespace: dict) -> bool:
    """Assert chart labels have no literal curly braces (query 17 specific).

    Args:
        code: Generated Python code string (unused but required by interface).
        namespace: Execution namespace containing __fig__ matplotlib figure.

    Returns:
        True if no curly braces found in labels.

    Raises:
        AssertionError: If any label contains curly braces.
    """
    fig = namespace["__fig__"]
    for ax in fig.axes:
        for text in ax.texts:
            label = text.get_text()
            assert (
                "{" not in label and "}" not in label
            ), f"Label contains literal curly braces: {label!r}"
    return True


def _assert_line_chart_and_no_curly_braces(code: str, namespace: dict) -> bool:
    """Assert chart has lines and no literal curly braces (query 23 specific).

    Args:
        code: Generated Python code string (unused but required by interface).
        namespace: Execution namespace containing __fig__ matplotlib figure.

    Returns:
        True if chart has lines and no curly braces in labels.

    Raises:
        AssertionError: If chart has no lines or labels contain curly braces.
    """
    fig = namespace["__fig__"]
    for ax in fig.axes:
        assert len(ax.lines) > 0, "Chart has no lines — expected a line chart"
        for text in ax.texts:
            label = text.get_text()
            assert (
                "{" not in label and "}" not in label
            ), f"Text contains literal curly braces: {label!r}"
    return True


# =============================================================================
# Tests
# =============================================================================


def test_standard_case(record: dict) -> None:
    """Evaluate standard quality criteria for non-specialized queries.

    Metrics:
        - has_answer: Non-empty response present
        - completeness_score: LLM-judged score >= 3.0 (scale 1-3)
        - resolution_rate: Chart passes bar chart + no curly braces assertion

    Args:
        record: Test case record dictionary containing query, answer, trajectory.
    """
    evaluator = AgentEvaluator(query_id=int(record["query_id"]))

    has_answer = evaluator.metric_has_answer(record)
    completeness_score = evaluator.metric_completeness_score(record)
    resolution_rate = evaluator.metric_resolution_rate(
        record, assertion=_assert_bar_chart_and_no_curly_braces
    )

    assert has_answer is True, "Agent produced empty answer"
    assert (
        completeness_score >= 3.0
    ), f"Completeness score {completeness_score} below threshold 3.0"
    assert resolution_rate is True, "Resolution rate failed"


def test_resolution_query_17(record: dict) -> None:
    """Query 17: Resolution rate with no-curly-braces-only assertion.

    Args:
        record: Test case record dictionary.
    """
    evaluator = AgentEvaluator(query_id=17)
    assert (
        evaluator.metric_resolution_rate(record, assertion=_assert_no_curly_braces_only)
        is True
    ), "Resolution rate failed"


def test_resolution_query_23(record: dict) -> None:
    """Query 23: Resolution rate with line-chart + no-curly-braces assertion.

    Args:
        record: Test case record dictionary.
    """
    evaluator = AgentEvaluator(query_id=23)
    assert (
        evaluator.metric_resolution_rate(
            record, assertion=_assert_line_chart_and_no_curly_braces
        )
        is True
    ), "Resolution rate failed"
