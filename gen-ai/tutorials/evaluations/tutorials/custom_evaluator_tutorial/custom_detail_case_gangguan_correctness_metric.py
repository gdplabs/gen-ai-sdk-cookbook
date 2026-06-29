from deepeval.test_case import LLMTestCaseParams
from gllm_evals.metrics.deepeval_geval import DeepEvalGEvalMetric
from gllm_evals.types import LLMTestCase, MetricScore
from gllm_inference.lm_invoker.lm_invoker import BaseLMInvoker


class CustomDetailCaseGangguanCorrectnessMetric(DeepEvalGEvalMetric):
    """Custom detail case gangguan correctness metric.

    Required Fields:
    - query (str): The query to evaluate the metric.
    - generated_response (str): The generated response to evaluate the metric.

    Attributes:
        name (str): The name of the metric.
        models (BaseLMInvoker | list[BaseLMInvoker] | None): The model invoker(s) to use for the metric.
        criteria (str | None): The criteria to use for the metric.
        evaluation_steps (list[str] | None): The evaluation steps to use for the metric.
        rubric (list[Rubric] | None): The rubric to use for the metric.
        threshold (float): The threshold to use for the metric.

    """

    def __init__(  # noqa: PLR0913
        self,
        models: BaseLMInvoker | list[BaseLMInvoker] | None = None,
        criteria: str | None = None,
        evaluation_steps: list[str] | None = None,
        threshold: float = 0.5,
        evaluation_params: list[LLMTestCaseParams] | None = None,
    ):
        """Initialize the GEval Completeness Metric.

        Args:
            models (BaseLMInvoker | list[BaseLMInvoker] | None): The model invoker(s) to use for the metric.
            criteria (str | None, optional): The criteria to use for the metric. default is DEFAULT_CRITERIA
            evaluation_steps (list[str] | None, optional): The evaluation steps to use for the metric. default
                is DEFAULT_EVALUATION_STEPS
            threshold (float, optional): The threshold to use for the metric. default is 0.5
            evaluation_params (list[LLMTestCaseParams] | None, optional): The evaluation parameters to use for the
                metric. default is [LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT]
        """
        super().__init__(
            name="detail_case_gangguan_correctness",
            models=models,
            criteria=criteria,
            evaluation_steps=evaluation_steps,
            threshold=threshold,
            evaluation_params=[
                LLMTestCaseParams.INPUT,
                LLMTestCaseParams.ACTUAL_OUTPUT,
            ],
        )

    async def _evaluate(self, data: LLMTestCase) -> MetricScore:
        """Evaluates the metric.

        Args:
            data (LLMTestCase): The metric input.

        Returns:
            MetricScore: The metric output.
        """
        output = await super()._evaluate(data)
        output.score = int(output.score)
        return output
