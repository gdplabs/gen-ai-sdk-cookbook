"""Completeness metric."""

import os

from dotenv import load_dotenv
from gllm_evals.metrics import GEvalCompletenessMetric
from gllm_evals.prompts.geval_generation_prompt import (
    COMPLETENESS_EVALUATION_STEPS,
)

import logging

logger = logging.getLogger(__name__)


def _build_metric() -> GEvalCompletenessMetric:
    STEP_7 = """
Step 7. Currency and Unit Validation (Post-Scoring Check)
After determining your score from Steps 1-6, apply this final check:
A. If the Expected Response presents values separated by currency, unit, or
   category (e.g., "US$715M in USD" and "€74M in EUR"), verify that the
   Generated Response does NOT combine values across different currencies or
   units into a single total. If it does, reclassify the affected key facts
   as Contradicted and reapply Step 5A (Contradiction Rule → Score = 1).
B. If the Expected Response presents data grouped by currency or unit (e.g.,
   USD group, EUR group, NZD group, GBP group), and the Generated Response
   omits one or more entire groups, reclassify ALL values in each omitted
   group as Missing and reapply Step 5C (Coverage Rule). Each currency/unit
   group in the Expected Response is a Minimum Key Fact — do NOT dismiss
   omitted groups as "supplementary" under Step 2B.
""".strip().splitlines()
    STEP_8 = """
Step 8. Structured Data Completeness (Post-Scoring Check)
After determining your score from Steps 1-7, apply this final check:
A. If the Expected Response contains a table, structured list, grouped list,
   categorized data, or multi-column data, classify each column or dimension
   into one of two categories:
   - Answer Dimensions: columns whose values directly answer the question
     (e.g., numeric amounts, dates, names the question asks about). These
     are Minimum Key Facts.
   - Contextual Labels: columns that provide metadata or categorization but
     do not themselves answer the question (e.g., a "Round" label like
     "Seed" when the question asks about price, or a "Currency" column when
     all values share the same currency). These are Supporting Facts —
     omitting them alone should NOT reduce the score.
B. If the Generated Response omits an Answer Dimension column (e.g., the
   Expected Response has both "Pre-Money Valuation" and "Current Valuation"
   but the Generated Response only includes one), reclassify the omitted
   values as Missing and reapply Step 5C (Coverage Rule).
C. If the Expected Response groups data by a meaningful partitioning category
   (e.g., separate currency groups: USD, EUR, NZD, GBP), each group is a
   Minimum Key Fact. Omitting entire groups means Missing — apply Step 5C.
D. To distinguish Answer Dimensions from Contextual Labels, ask: "Does
   omitting this column cause the response to miss part of the ANSWER to
   the question?" If yes → Minimum Key Fact. If the answer is still
   complete without it → Supporting Fact.
""".strip().splitlines()
    STEP_9 = """
Step 9. Numeric Rounding Tolerance (Post-Scoring Check)
After determining your score from Steps 1-8, apply this final check:
A. This rule ONLY applies to abbreviated or scaled numeric formats where a
   unit suffix indicates magnitude (e.g., "$76.57M", "2.4B", "12.2K").
   When BOTH the Expected and Generated values use such abbreviated formats,
   treat minor rounding differences as Matched — NOT Missing or Contradicted
   — provided the rounding error is ≤ 1% of the expected value.
   Examples that MATCH: $76.57M ≈ $76.6M, $37.78M ≈ $37.8M, $12.24M ≈ $12.2M.
B. This rule does NOT apply to full literal numbers (e.g., 118,445,462 or
   254,486,317.0). When the Expected Response uses unabbreviated literal
   values, the Generated Response must reproduce the full number exactly.
   Truncating or rounding literal digits (e.g., 118,445,462 → 118,445,000)
   is a loss of precision and must be classified as Contradicted.
C. Only override Step 3E when the Generated Response clearly reformatted the
   Expected Response value into an abbreviated form with acceptable rounding
   (per rule A), not when literal digits were dropped.
""".strip().splitlines()
    STEP_10 = """
Step 10. Data vs. Narrative Precedence (Post-Scoring Check)
After determining your score from Steps 1-9, apply this final check:
A. If the Expected Response contains BOTH structured data (tables, lists with
   numbers) AND a narrative interpretation (insights, trend descriptions),
   and the narrative contradicts the actual data values, then the DATA is
   the authoritative ground truth — not the narrative.
B. If the Generated Response derives a conclusion that correctly follows from
   the Expected Response's data but contradicts the Expected Response's
   narrative interpretation, do NOT classify this as a Contradiction.
   Example: if the Expected Response's table shows Current Valuation dropping
   from 58B to 40B, but the narrative says "current valuation continued to
   grow", the Generated Response is correct to report a decline. The
   narrative was erroneous; the data is ground truth.
C. Only apply Step 5A (Contradiction Rule) when the Generated Response
   contradicts the Expected Response's DATA, not when it contradicts an
   incorrect narrative summary within the Expected Response.
""".strip().splitlines()
    load_dotenv()
    final_evaluation_steps = COMPLETENESS_EVALUATION_STEPS + STEP_7 + STEP_8 + STEP_9 + STEP_10
    return GEvalCompletenessMetric(
        model_credentials=os.getenv("GOOGLE_API_KEY"), evaluation_steps=final_evaluation_steps
    )


async def completeness_score(records: dict | list[dict]) -> float | list[float]:
    """Return LLM-based completeness score(s) (1-3) using GEvalGenerationEvaluator.

    Accepts a single record dict or a list of record dicts. Each dict should have
    'query', 'answer', and 'expected_answer' keys.

    Returns:
        float when a single record is given, list[float] for a list.
    """
    metric = _build_metric()
    single = isinstance(records, dict)
    items = [records] if single else records

    rag_items = [
        {
            "query":r.get("query", ""),
            "expected_response":r.get("expected_answer", ""),
            "generated_response":r.get("answer", ""),
        }
        for r in items
    ]

    try:
        scores = await metric.evaluate(rag_items)
        logger.info(f"Completeness score(s): {scores}")
        logger.info(f"Single: {single}")
        if single:
            return float(next(iter(scores))["geval_completeness"]["score"])
        return [float(v["geval_completeness"]["score"]) for v in scores]
    except Exception as e:
        logger.warning(f"Failed to compute completeness score: {e}. Returning 1.0.")
        return 1.0 if single else [1.0] * len(items)
