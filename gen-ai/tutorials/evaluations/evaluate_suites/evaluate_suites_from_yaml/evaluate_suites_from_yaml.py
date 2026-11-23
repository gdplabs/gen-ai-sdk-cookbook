"""Evaluate one standard suite loaded from YAML."""

import asyncio
import json
from pathlib import Path

from dotenv import load_dotenv
from gllm_evals import EvalSuite, evaluate_suites
from gllm_evals.utils.yaml_suite_loader import register_metric_class
from metrics.custom_metrics import KeywordMatchMetric

load_dotenv()

EXAMPLE_ROOT = Path(__file__).resolve().parent


async def main() -> None:
    """Register a metric, load one YAML file, and evaluate it."""
    register_metric_class("RegisteredKeywordMatchMetric", KeywordMatchMetric)
    suite = EvalSuite.from_yaml(
        EXAMPLE_ROOT / "sample_suites" / "custom_judge_model_and_metrics_suite.yaml"
    )
    result = await evaluate_suites(suites=[suite], dataset_name="standard_yaml")
    print(json.dumps(result.model_dump(), indent=2))


if __name__ == "__main__":
    asyncio.run(main())
