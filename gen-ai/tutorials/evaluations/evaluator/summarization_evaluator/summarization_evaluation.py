"""SummarizationEvaluator Tutorial.

This tutorial demonstrates how to use SummarizationEvaluator
to evaluate the quality of generated summaries.

By default, SummarizationEvaluator runs four metrics:
- coherence, consistency, relevance, and fluency.
"""

import asyncio
import json

from gllm_evals import LLMTestCase
from gllm_evals.evaluator.summarization_evaluator import SummarizationEvaluator


async def main() -> None:
    """Run a summarization evaluation example."""
    data = LLMTestCase(
        input="Meeting transcript or source text here...",
        actual_output="Generated summary here...",
    )

    evaluator = SummarizationEvaluator()
    result = await evaluator.evaluate(data)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
