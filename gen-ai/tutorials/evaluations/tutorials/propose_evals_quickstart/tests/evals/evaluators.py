"""Which metrics score each suite of the Banking Assistant Chatbot eval.

The only place that builds metrics and evaluators. Reasons live in metric-assignment.md.
"""

import os

from gllm_evals.evaluator.composite_evaluator import CompositeEvaluator
from gllm_evals.evaluator.evaluator import BaseEvaluator
from gllm_evals.metrics.generation import (
    GEvalCompletenessMetric,
    GEvalGroundednessMetric,
    GEvalLanguageConsistencyMetric,
    GEvalRefusalAlignmentMetric,
)
from gllm_inference.dm_invoker import build_dm_invoker

GROUNDEDNESS_INFO = (
    "The retrieved context is the bank-policy context that was supplied to the assistant together with the question; "
    "it is the only source the assistant may answer from. It may contain HTML tables and several documents separated "
    "by '###'. When a table shows a before/after change, the assistant is instructed to use the newest value."
)


def _jev():
    """Jev 1.14, the judge for every GEval metric (references/choosing-metrics.md, "Judge model")."""
    return build_dm_invoker(
        model_id="openrouter/typesafe/jev-1.14",
        credentials=os.getenv("OPENROUTER_API_KEY"),
        config={"provider": {"order": ["typesafe"], "allow_fallbacks": False}},
    )


def build_evaluators() -> dict[str, list[BaseEvaluator]]:
    """Map each suite to its one evaluator, built fresh on each call."""
    jev = _jev()
    return {
        "answerable": [
            CompositeEvaluator(
                name="answerable",
                metrics=[
                    GEvalCompletenessMetric(models=jev),  # R1, threshold 1.0 (default)
                    GEvalGroundednessMetric(models=jev, additional_info=GROUNDEDNESS_INFO),  # R2, threshold 1.0
                    GEvalLanguageConsistencyMetric(models=jev),  # R3, threshold 0.5 (default)
                ],
            )
        ],
        "refusal": [
            CompositeEvaluator(
                name="refusal",
                metrics=[GEvalRefusalAlignmentMetric(models=jev)],  # R4, threshold 0.5 (default)
            )
        ],
    }
