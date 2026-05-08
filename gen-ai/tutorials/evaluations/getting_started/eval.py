import asyncio

from gllm_evals import LLMTestCase
from gllm_evals.metrics import GEvalCompletenessMetric


async def main() -> None:
    """Run a simple evaluation example."""
    metric = GEvalCompletenessMetric()
    data = LLMTestCase(
        input="What is the capital of France?",
        actual_output="New York",
        expected_output="Paris is the capital of France.",
    )
    result = await metric.evaluate(data)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
