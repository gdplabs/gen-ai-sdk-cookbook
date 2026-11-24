import asyncio

from approach3_order_exists_metric import OrderExistsInDBMetric
from gllm_evals.types import LLMTestCase, ToolCall


async def main():
    mock_db = {"order_1001": {"status": "created"}}
    metric = OrderExistsInDBMetric(mock_db=mock_db)

    data = LLMTestCase(
        input="Create an order for user_1 with coffee_beans quantity 1.",
        actual_output="Order order_1001 has been created.",
        order_id="order_1001",
        tools_called=[
            ToolCall(
                name="create_order",
                input_parameters={
                    "user_id": "user_1",
                    "product_id": "coffee_beans",
                    "quantity": 1,
                },
            )
        ],
    )

    result = await metric.evaluate(data)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
