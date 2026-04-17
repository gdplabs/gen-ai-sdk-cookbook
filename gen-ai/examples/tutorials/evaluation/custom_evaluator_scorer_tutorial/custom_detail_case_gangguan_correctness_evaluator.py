from gllm_evals.evaluator.evaluator import BaseEvaluator
from gllm_evals.types import MetricInput, MetricOutput

from custom_detail_case_gangguan_correctness_metric import (
    CustomDetailCaseGangguanCorrectnessMetric,
)
from evaluation_steps import CUSTOM_DETAIL_CASE_GANGGUAN_CORRECTNESS_EVALUATION_STEPS


class CustomDetailCaseGangguanCorrectnessEvaluator(BaseEvaluator):
    """Custom detail case gangguan correctness evaluator."""

    def __init__(self, model_credentials: str, threshold: float = 0.5):
        """Initialize the CustomDetailCaseGangguanCorrectnessEvaluator.

        Args:
            model_credentials (str): The model credentials.
            threshold (float, optional): The threshold to use for the metric.
        """
        super().__init__(name="custom_detail_case_gangguan_correctness_evaluator")
        self.metric = CustomDetailCaseGangguanCorrectnessMetric(
            model_credentials=model_credentials,
            evaluation_steps=CUSTOM_DETAIL_CASE_GANGGUAN_CORRECTNESS_EVALUATION_STEPS,
            threshold=threshold,
        )

    async def _evaluate(self, data: MetricInput) -> MetricOutput:
        """Evaluate detail case gangguan correctness.

        Args:
            data (MetricInput): The input data containing query and generated_response.

        Returns:
            MetricOutput: The evaluation output with score and explanation.
        """
        return await self.metric.evaluate(data)
