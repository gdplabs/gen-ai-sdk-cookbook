from gllm_evals.metrics.metric import BaseMetric
from gllm_evals.types import LLMTestCase, MetricScore


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

    async def _evaluate(self, data: LLMTestCase) -> MetricScore:
        order_id = getattr(data, "order_id", None)
        if not isinstance(order_id, str):
            return MetricScore(
                score=0.0,
                explanation="Invalid or missing order_id",
            )

        exists = order_id in self.mock_db
        return MetricScore(
            score=1.0 if exists else 0.0,
            explanation=None
            if exists
            else f"Order {order_id} not found in DB",
        )
