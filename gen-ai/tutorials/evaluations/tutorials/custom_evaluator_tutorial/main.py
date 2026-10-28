import asyncio
import os

import pandas as pd
from custom_detail_case_gangguan_correctness_evaluator import (
    CustomDetailCaseGangguanCorrectnessEvaluator,
)
from gllm_evals import LLMTestCase
from gllm_evals.dataset.dict_dataset import DictDataset
from gllm_inference.lm_invoker import build_lm_invoker


async def main():
    """Evaluate custom detail case gangguan correctness using LLM-as-a-judge."""

    # Initialize the custom evaluator we have just created above, with DeepSeek (via OpenRouter) as the judge
    evaluator = CustomDetailCaseGangguanCorrectnessEvaluator(
        models=build_lm_invoker(
            model_id="openrouter/deepseek/deepseek-v4.1-flash-1017",
            credentials=os.getenv("OPENROUTER_API_KEY"),
            config={"provider": {"order": ["inference.net"], "allow_fallbacks": False}},
        ),
        threshold=0.75,
    )

    # Load the JSONL dataset using DictDataset
    # Also loads from CSV: DictDataset.from_csv(...)
    dataset = DictDataset.from_jsonl("tsel_test_data.jsonl").load()

    final_results = []
    alignment_scores = []
    for row in dataset:
        # Each row is an LLMTestCase; the JSON keys are extra fields.
        data = LLMTestCase(
            input=row.detailed_description,
            actual_output=row.detail_case_gangguan,
        )
        result = await evaluator.evaluate(data)
        # The metric result is an extra field of the evaluator's EvaluatorOutput.
        metric_result = result[evaluator.name].model_extra["detail_case_gangguan_correctness"]
        final_results.append(
            {
                "no": row.no,
                "query": row.detailed_description,
                "generated_response": row.detail_case_gangguan,
                "score": metric_result.score,
                "explanation": metric_result.explanation,
                "gt_score": row.score_detail_case_gangguan,
                "is_aligned": row.score_detail_case_gangguan == metric_result.score,
            }
        )
        alignment_scores.append(int(final_results[-1]["is_aligned"]))

    # Export the data with the evaluation results as CSV
    pd.DataFrame(final_results).to_csv(
        "final_results_detail_case_gangguan_correctness.csv", index=False
    )

    # Optional Step - Calculate the alignment scores between LLM-as-a-judge and ground truth evaluation
    final_alignment_score = (
        sum(alignment_scores) / len(alignment_scores) if alignment_scores else 0.0
    )
    print(f"Alignment score: {final_alignment_score * 100}%")


if __name__ == "__main__":
    asyncio.run(main())
