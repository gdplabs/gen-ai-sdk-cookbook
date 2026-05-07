import asyncio
import os

import pandas as pd
from custom_detail_case_gangguan_correctness_evaluator import (
    CustomDetailCaseGangguanCorrectnessEvaluator,
)
from gllm_evals import LLMTestCase
from gllm_evals.dataset.dict_dataset import DictDataset


async def main():
    """Evaluate custom detail case gangguan correctness using LLM-as-a-judge."""

    # Initialize the custom evaluator we have just created above
    evaluator = CustomDetailCaseGangguanCorrectnessEvaluator(
        model_credentials=os.getenv("GOOGLE_API_KEY"),
        threshold=0.75,
    )

    # Load the CSV dataset using DictDataset
    csv_path = "/path/to/tsel_test_data.csv"
    dataset = DictDataset.from_csv(csv_path).load()

    final_results = []
    alignment_scores = []
    for row in dataset:
        data = LLMTestCase(
            input=row["detailed_description"],
            actual_output=row["detail_case_gangguan"],
        )
        result = await evaluator.evaluate(data)
        final_results.append(
            {
                "no": row["no"],
                "query": row["detailed_description"],
                "generated_response": row["detail_case_gangguan"],
                "score": result[evaluator.name]["detail_case_gangguan_correctness"].get(
                    "score", 0
                ),
                "explanation": result[evaluator.name][
                    "detail_case_gangguan_correctness"
                ].get("explanation", ""),
                "gt_score": row["score_detail_case_gangguan"],
                "is_aligned": row["score_detail_case_gangguan"]
                == result[evaluator.name]["detail_case_gangguan_correctness"].get(
                    "score", 0
                ),
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
