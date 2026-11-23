from gllm_evals.metrics.metric import BaseMetric
from gllm_evals.types import LLMTestCase, MetricScore

_ORDER_ID_FIELD = "order_id"


class OrderExistsInDBMetric(BaseMetric):
    """Check whether an order ID exists in a mock database.

    ``order_id`` is an extra ``LLMTestCase`` field, not one of the fixed columns.
    """

    required_fields: set[str] = {_ORDER_ID_FIELD}
    input_type: type = LLMTestCase
    higher_is_better: bool = True

    def __init__(
        self,
        mock_db: dict[str, dict[str, str]] | None = None,
    ):
        self.name = "order_exists_in_db"
        self.mock_db = mock_db or {}

    async def _evaluate(self, data: LLMTestCase) -> MetricScore:
        order_id = getattr(data, _ORDER_ID_FIELD)
        if not isinstance(order_id, str):
            return MetricScore(score=0.0, explanation="Invalid or missing order_id")

        exists = order_id in self.mock_db
        return MetricScore(
            score=1.0 if exists else 0.0,
            explanation=None if exists else f"Order {order_id} not found in DB",
        )
