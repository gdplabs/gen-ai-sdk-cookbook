"""QueryTransformerEvaluator Tutorial.

This tutorial demonstrates how to use QTEvaluator
to evaluate query transformation quality.
"""

import asyncio

from gllm_evals.evaluator.qt_evaluator import QTEvaluator
from gllm_evals.types import LLMTestCase


async def main() -> None:
    """Run a query transformer evaluation example."""
    qt_task_prefix = "Decompose this query: "
    query = "Siapa yang bertanggung jawab atas pemantauan kepatuhan terintegrasi dan bagaimana cara melaporkannya?"
    query = f"{qt_task_prefix}{query}"

    expected_response = [
        "penanggung jawab pemantauan kepatuhan terintegrasi",
        "prosedur pelaporan kepatuhan terintegrasi",
    ]
    generated_response = [
        "penanggung jawab pemantauan kepatuhan terintegrasi",
        "prosedur pelaporan kepatuhan terintegrasi",
    ]

    data = LLMTestCase(
        input=query,
        expected_output=str(expected_response),
        actual_output=str(generated_response),
    )

    evaluator = QTEvaluator()
    result = await evaluator.evaluate(data)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
