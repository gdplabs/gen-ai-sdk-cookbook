import asyncio
import json
import os

from gllm_evals import LLMTestCase
from gllm_evals.evaluator.summarization_evaluator import SummarizationEvaluator
from gllm_inference.lm_invoker import build_lm_invoker


async def main() -> None:
    """Run a summarization evaluation example."""
    data = LLMTestCase(
        input="Meeting transcript or source text here...",
        actual_output="Generated summary here...",
    )

    evaluator = SummarizationEvaluator(
        models=build_lm_invoker(
            model_id="openrouter/deepseek/deepseek-v4.1-flash-1017",
            credentials=os.getenv("OPENROUTER_API_KEY"),
            config={"provider": {"order": ["inference.net"], "allow_fallbacks": False}},
        )
    )
    result = await evaluator.evaluate(data)
    print(json.dumps({name: output.model_dump(mode="json") for name, output in result.items()}, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
