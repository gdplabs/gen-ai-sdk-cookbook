"""Evaluate every YAML suite in a directory."""

import asyncio
import json
import sys
from pathlib import Path

from gllm_evals import EvalSuite, evaluate_suites
from gllm_evals.utils.yaml_suite_loader import register_metric_class

EXAMPLE_ROOT = Path(__file__).resolve().parent
if str(EXAMPLE_ROOT) not in sys.path:
    sys.path.insert(0, str(EXAMPLE_ROOT))

from metrics.custom_metrics import KeywordMatchMetric  # noqa: E402


async def main() -> None:
    """Load all sample suites and evaluate them together."""
    register_metric_class("RegisteredKeywordMatchMetric", KeywordMatchMetric)
    suite_dir = EXAMPLE_ROOT / "sample_suites"
    suites = EvalSuite.from_yaml_dir(suite_dir)
    result = await evaluate_suites(suites=suites, dataset_name="yaml_directory")
    print(json.dumps(result.model_dump(), indent=2))


if __name__ == "__main__":
    asyncio.run(main())
