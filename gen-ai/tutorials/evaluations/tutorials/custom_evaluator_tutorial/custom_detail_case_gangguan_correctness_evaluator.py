from custom_detail_case_gangguan_correctness_metric import (
    CustomDetailCaseGangguanCorrectnessMetric,
)
from evaluation_steps import CUSTOM_DETAIL_CASE_GANGGUAN_CORRECTNESS_EVALUATION_STEPS
from gllm_evals.evaluator.evaluator import BaseEvaluator
from gllm_evals.types import EvaluatorResult, MetricInput
from gllm_inference.lm_invoker.lm_invoker import BaseLMInvoker


class CustomDetailCaseGangguanCorrectnessEvaluator(BaseEvaluator):
    """Custom detail case gangguan correctness evaluator."""

    def __init__(
        self,
        models: BaseLMInvoker | list[BaseLMInvoker] | None = None,
        threshold: float = 0.5,
    ):
        """Initialize the CustomDetailCaseGangguanCorrectnessEvaluator.

        Args:
            models (BaseLMInvoker | list[BaseLMInvoker] | None): The model invoker(s).
            threshold (float, optional): The threshold to use for the metric.
        """
        super().__init__(name="custom_detail_case_gangguan_correctness_evaluator")
        self.metric = CustomDetailCaseGangguanCorrectnessMetric(
            models=models,
            evaluation_steps=CUSTOM_DETAIL_CASE_GANGGUAN_CORRECTNESS_EVALUATION_STEPS,
            threshold=threshold,
        )

    async def _evaluate(self, data: MetricInput) -> EvaluatorResult:
        """Evaluate detail case gangguan correctness.

        Args:
            data (MetricInput): The input data containing input and actual_output.

        Returns:
            EvaluatorResult: The evaluation output with score and explanation.
        """
        return {self.metric.name: await self.metric.evaluate(data)}
