import asyncio
import os

from approach2_politeness_metric import PolitenessMetric
from gllm_evals.types import LLMTestCase
from gllm_inference.lm_invoker import build_lm_invoker


async def main():
    data = LLMTestCase(
        input="Can you help me reset my password?",
        actual_output="Hello! Thank you for contacting us. I'd be happy to help you reset your password.",
    )

    metric = PolitenessMetric(
        models=build_lm_invoker(
            model_id="openrouter/deepseek/deepseek-v4.1-flash-1017",
            credentials=os.getenv("OPENROUTER_API_KEY"),
            config={"provider": {"order": ["inference.net"], "allow_fallbacks": False}},
        )
    )
    result = await metric.evaluate(data)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
