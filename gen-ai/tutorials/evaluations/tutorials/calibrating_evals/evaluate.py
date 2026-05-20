import asyncio
import json
import os
from dotenv import load_dotenv
from gllm_inference.lm_invoker import build_lm_invoker

from gllm_evals import LLMTestCase
from gllm_evals.dataset.dict_dataset import DictDataset
from gllm_evals.evaluate import evaluate
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.experiment_tracker import CSVExperimentTracker
from gllm_evals.constant import DefaultValues

from aggregators import _make_true_negative_rate, _make_true_positive_rate

load_dotenv()


async def main() -> None:
    # ========================================================================
    # Load dataset from Google Sheets
    # ========================================================================

    dataset = await DictDataset.from_gsheets(
        sheet_id="1CVWqNzX_tdnvkV0fQ3NPDuEE9HtTXk8k2XtgIg6Ml6M",
        worksheet_name="calibrate-dataset-simplified",
        client_email=os.getenv("GOOGLE_SHEETS_CLIENT_EMAIL"),
        private_key=os.getenv("GOOGLE_SHEETS_PRIVATE_KEY"),
    )

    # ========================================================================
    # Build test cases with labels
    # ========================================================================

    data = [
        LLMTestCase(
            input=row["input"],
            actual_output=row["actual_output"],
            expected_output=row["expected_output"],
            retrieved_context=row["retrieved_context"],
            label=row["label"],
        )
        for row in dataset.load()
    ]

    # ========================================================================
    # Configure evaluator and experiment tracker
    # ========================================================================

    evaluator = GEvalGenerationEvaluator(
        models=build_lm_invoker(
            model_id=DefaultValues.MODEL,
        )
    )
    experiment_tracker = CSVExperimentTracker(
        project_name="calibration",
        output_dir="calibration",
        extra_score_keys=["aggregate_score", "aggregate_success", "aggregate"],
        companion_fields=["success", "explanation"],
        include_eval_result=True,
    )
    evaluator.refusal_metric = None

    # ========================================================================
    # Run evaluation with metrics aggregation
    # ========================================================================

    results = await evaluate(
        data=data,
        evaluators=[evaluator],
        run_aggregators=[
            _make_true_negative_rate("generation"),
            _make_true_positive_rate("generation"),
        ],
        experiment_tracker=experiment_tracker,
    )

    # ========================================================================
    # Output results and metrics
    # ========================================================================

    print(json.dumps(results["results"], indent=2))
    print(json.dumps(results["run_aggregators_result"], indent=2))


if __name__ == "__main__":
    asyncio.run(main())
