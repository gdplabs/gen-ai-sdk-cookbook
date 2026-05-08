from deepeval.metrics.g_eval import Rubric
from deepeval.test_case import LLMTestCaseParams
from gllm_evals.constant import ColumnNames
from gllm_evals.metrics.deepeval_geval import DeepEvalGEvalMetric, MetricDefaults
from gllm_evals.types import LLMTestCase


class PolitenessMetric(DeepEvalGEvalMetric):
    """Custom metric evaluating politeness of responses."""

    description: str = "Politeness score. Normalized to [0, 1] range."
    required_fields: set[str] = {
        ColumnNames.INPUT,
        ColumnNames.ACTUAL_OUTPUT,
    }
    input_type: type = LLMTestCase
    higher_is_better: bool = True

    _defaults = MetricDefaults(
        name="geval_politeness",
        criteria="Politeness (1-3) - Assess how polite the response is.",
        rubric=[
            Rubric(score_range=(1, 1), expected_outcome="Rude"),
            Rubric(score_range=(2, 2), expected_outcome="Neutral"),
            Rubric(score_range=(3, 3), expected_outcome="Polite"),
        ],
        evaluation_params=[
            LLMTestCaseParams.INPUT,
            LLMTestCaseParams.ACTUAL_OUTPUT,
        ],
    )

    def _to_rubric_score(self, raw: float) -> int:
        return int(1 + raw * 2)
