"""Custom metrics used by the YAML evaluation examples."""

from gllm_evals.constant import ColumnNames
from gllm_evals.metrics.metric import BaseMetric
from gllm_evals.types import LLMTestCase, MetricScore


class ExactMatchMetric(BaseMetric):
    """Deterministic exact-match metric: scores 1.0 if actual_output == expected_output.

    No judge model, no network call — the score is computed with a plain string
    comparison, so it's free, instant, and exactly reproducible.

    Attributes:
        name (str): The name of the metric.
        required_fields (set[str]): actual_output and expected_output must both be present.
        higher_is_better (bool): Always True — a match is always the better outcome.
        threshold (float): 1.0 by default, so only an exact match counts as success.
        case_sensitive (bool): Whether comparison is case-sensitive. Defaults to False.
    """

    required_fields: set[str] = {ColumnNames.ACTUAL_OUTPUT, ColumnNames.EXPECTED_OUTPUT}
    input_type: type = LLMTestCase
    higher_is_better: bool = True

    def __init__(
        self,
        name: str = "exact_match",
        threshold: float = 1.0,
        case_sensitive: bool = False,
    ):
        """Initialize the ExactMatchMetric.

        Args:
            name (str, optional): The name of the metric. Defaults to "exact_match".
            threshold (float, optional): Pass/fail threshold in [0, 1]. Defaults to 1.0
                (only an exact match succeeds).
            case_sensitive (bool, optional): Whether comparison is case-sensitive.
                Defaults to False.
        """
        self.name = name
        self.threshold = threshold
        self.case_sensitive = case_sensitive

    async def _evaluate(self, data: LLMTestCase) -> MetricScore:
        """Compare actual_output to expected_output with a plain string comparison.

        Args:
            data (LLMTestCase): The data to evaluate. actual_output/expected_output
                are guaranteed non-None here (enforced by required_fields/can_evaluate).

        Returns:
            MetricScore: 1.0 on an exact match, 0.0 otherwise.
        """
        actual = data.actual_output.strip()
        expected = data.expected_output.strip()
        if not self.case_sensitive:
            actual, expected = actual.lower(), expected.lower()

        is_match = actual == expected
        explanation = (
            "actual_output matches expected_output exactly"
            if is_match
            else (
                f"actual_output {data.actual_output!r} does not match expected_output {data.expected_output!r}"
            )
        )
        return MetricScore(score=1.0 if is_match else 0.0, explanation=explanation)


class KeywordMatchMetric(BaseMetric):
    """Score whether the expected output appears in the actual output."""

    required_fields: set[str] = {ColumnNames.ACTUAL_OUTPUT, ColumnNames.EXPECTED_OUTPUT}
    input_type: type = LLMTestCase
    higher_is_better: bool = True

    def __init__(self, name: str = "keyword_match", threshold: float = 1.0) -> None:
        self.name = name
        self.threshold = threshold

    async def _evaluate(self, data: LLMTestCase) -> MetricScore:
        expected = data.expected_output.strip().lower()
        actual = data.actual_output.strip().lower()
        is_match = expected in actual
        return MetricScore(
            score=1.0 if is_match else 0.0,
            explanation="Expected output appears in actual output"
            if is_match
            else "Expected output does not appear in actual output",
        )
