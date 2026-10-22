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

    # Build the judge model invoker (MiMo via OpenRouter) and pass it to the evaluator
    invoker = build_lm_invoker(
        model_id="openrouter/xiaomi/mimo-v2.6-flash",
        credentials=os.getenv("OPENROUTER_API_KEY"),
        config={"provider": {"order": ["makora"], "allow_fallbacks": False}},
    )

    # Initialize the custom evaluator we have just created above
    evaluator = CustomDetailCaseGangguanCorrectnessEvaluator(
        models=invoker,
        threshold=0.75,
    )

    # Load the CSV dataset using DictDataset
    csv_path = "tsel_test_data.csv"
    dataset = DictDataset.from_csv(csv_path).load()

    final_results = []
    alignment_scores = []
    for row in dataset:
        data = LLMTestCase(
            input=row.detailed_description,
            actual_output=row.detail_case_gangguan,
        )
        result = await evaluator.evaluate(data)
        metric_result = (result[evaluator.name].model_extra or {}).get(
            "detail_case_gangguan_correctness"
        )
        score = metric_result.score if metric_result is not None else 0
        final_results.append(
            {
                "no": row.no,
                "query": row.detailed_description,
                "generated_response": row.detail_case_gangguan,
                "score": score,
                "explanation": metric_result.explanation if metric_result is not None else "",
                "gt_score": row.score_detail_case_gangguan,
                "is_aligned": row.score_detail_case_gangguan == score,
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
