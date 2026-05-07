import os
from typing import Any

from deepeval.test_case import LLMTestCaseParams
from gllm_inference.lm_invoker.lm_invoker import BaseLMInvoker
from gllm_inference.schema import ModelId

from gllm_evals.constant import DefaultValues
from gllm_evals.metrics.deepeval_geval import DeepEvalGEvalMetric
from gllm_evals.types import MetricInput, MetricOutput


class CustomDetailCaseGangguanCorrectnessMetric(DeepEvalGEvalMetric):
    """Custom detail case gangguan correctness metric.

    Required Fields:
    - query (str): The query to evaluate the metric.
    - generated_response (str): The generated response to evaluate the metric.

    Attributes:
        name (str): The name of the metric.
        model (str | ModelId | BaseLMInvoker): The model to use for the metric.
        model_credentials (str | None): The model credentials to use for the metric.
        model_config (dict[str, Any] | None): The model config to use for the metric.
        criteria (str | None): The criteria to use for the metric.
        evaluation_steps (list[str] | None): The evaluation steps to use for the metric.
        rubric (list[Rubric] | None): The rubric to use for the metric.
        threshold (float): The threshold to use for the metric.

    """

    def __init__(  # noqa: PLR0913
        self,
        model: str | ModelId | BaseLMInvoker = DefaultValues.MODEL,
        model_credentials: str | None = None,
        model_config: dict[str, Any] | None = None,
        criteria: str | None = None,
        evaluation_steps: list[str] | None = None,
        threshold: float = 0.5,
        evaluation_params: list[LLMTestCaseParams] | None = None,
    ):
        """Initialize the GEval Completeness Metric.

        Args:
            model (str | ModelId | BaseLMInvoker): The model to use for the metric.
            model_credentials (str | None): The model credentials to use for the metric.
            model_config (dict[str, Any] | None): The model config to use for the metric.
            criteria (str | None, optional): The criteria to use for the metric. default is DEFAULT_CRITERIA
            evaluation_steps (list[str] | None, optional): The evaluation steps to use for the metric. default
                is DEFAULT_EVALUATION_STEPS
            threshold (float, optional): The threshold to use for the metric. default is 0.5
            evaluation_params (list[LLMTestCaseParams] | None, optional): The evaluation parameters to use for the
                metric. default is [LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT]
        """
        super().__init__(
            name="detail_case_gangguan_correctness",
            model=model,
            model_credentials=model_credentials or os.getenv("GOOGLE_API_KEY"),
            model_config=model_config,
            criteria=criteria,
            evaluation_steps=evaluation_steps,
            threshold=threshold,
            evaluation_params=[
                LLMTestCaseParams.INPUT,
                LLMTestCaseParams.ACTUAL_OUTPUT,
            ],
        )

    async def _evaluate(self, data: MetricInput) -> MetricOutput:
        """Evaluates the metric.

        Args:
            data (MetricInput): The metric input.

        Returns:
            MetricOutput: The metric output.
        """
        output = await super()._evaluate(data)
        output["score"] = int(output["score"])
        return output
