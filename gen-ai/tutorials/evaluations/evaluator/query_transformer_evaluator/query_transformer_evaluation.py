import asyncio
import os

from gllm_evals.evaluator.qt_evaluator import QTEvaluator
from gllm_evals.types import LLMTestCase
from gllm_inference.lm_invoker import build_lm_invoker


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

    evaluator = QTEvaluator(
        models=build_lm_invoker(
            model_id="openrouter/deepseek/deepseek-v4.1-flash-1017",
            credentials=os.getenv("OPENROUTER_API_KEY"),
            config={"provider": {"order": ["inference.net"], "allow_fallbacks": False}},
        )
    )
    result = await evaluator.evaluate(data)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
