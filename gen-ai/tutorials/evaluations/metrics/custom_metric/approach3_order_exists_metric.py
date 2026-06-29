from gllm_evals.constant import ResultMetricKeys
from gllm_evals.metrics.metric import BaseMetric
from gllm_evals.types import LLMTestCase, MetricOutput


class OrderExistsInDBMetric(BaseMetric):
    """Check whether an order ID exists in a mock database."""

    name = "order_exists_in_db"
    required_fields = {"order_id"}

    def __init__(
        self,
        mock_db: dict[str, dict[str, str]] | None = None,
    ):
        super().__init__()
        self.mock_db = mock_db or {}

    async def _evaluate(self, data: LLMTestCase) -> MetricOutput:
        order_id = getattr(data, "order_id", None)
        if not isinstance(order_id, str):
            return {
                ResultMetricKeys.SCORE: 0.0,
                ResultMetricKeys.EXPLANATION: "Invalid or missing order_id",
            }

        exists = order_id in self.mock_db
        return {
            ResultMetricKeys.SCORE: 1.0 if exists else 0.0,
            ResultMetricKeys.EXPLANATION: None
            if exists
            else f"Order {order_id} not found in DB",
        }
