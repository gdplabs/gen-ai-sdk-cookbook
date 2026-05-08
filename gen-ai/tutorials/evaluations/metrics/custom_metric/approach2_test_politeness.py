import asyncio

from approach2_politeness_metric import PolitenessMetric
from gllm_evals.types import LLMTestCase


async def main():
    data = LLMTestCase(
        input="Can you help me reset my password?",
        actual_output="Hello! Thank you for contacting us. I'd be happy to help you reset your password.",
    )

    metric = PolitenessMetric()
    result = await metric.evaluate(data)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
