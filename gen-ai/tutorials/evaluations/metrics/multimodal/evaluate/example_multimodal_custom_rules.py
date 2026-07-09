import asyncio
import json

from gllm_evals import AttachmentRef, EvalSuite, LLMTestCase, evaluate_suites
from gllm_evals.evaluator.composite_evaluator import CompositeEvaluator
from gllm_evals.metrics import GEvalCompletenessMetric, GEvalGroundednessMetric

IMAGE_BASE_URL = (
    "https://raw.githubusercontent.com/gdplabs/gen-ai-sdk-cookbook/"
    "cd99df74b120982af30a495f1c549c5854801b46/gen-ai/tutorials/evaluations/assets/multimodal"
)
CHART_URI = f"{IMAGE_BASE_URL}/multimodal_sales_chart.png"

COMPLETENESS_RULES = """
When judging chart answers, inspect the image directly. Reward answers that name the requested month,
read the bar height from the Units Sold axis, and allow small visual-estimation variance. Penalize answers
that ignore the chart, use a different month, or invent exact values unsupported by the image.
""".strip()

GROUNDEDNESS_RULES = """
When judging grounding, verify every numeric claim against the chart image and retrieved visual context.
Accept approximate values only when they are consistent with the plotted bar and axis scale. Penalize claims
that contradict the visible chart even if the prose is otherwise fluent.
""".strip()


async def main() -> None:
    data = [
        LLMTestCase(
            input="How many units were sold in May according to this chart? [ATTACHMENT:sales_chart]",
            actual_output="The chart shows about 88 units sold in May.",
            expected_output="Around 88 units were sold in May, since the May bar sits just below 90 on the Units Sold axis.",
            retrieved_context=["Chart reference: [ATTACHMENT:sales_chart]"],
            attachments={"sales_chart": AttachmentRef(uri=CHART_URI, mime_type="image/png")},
        ),
        LLMTestCase(
            input="How many units were sold in May according to this chart? [ATTACHMENT:sales_chart]",
            actual_output="The chart shows 35 units sold in May.",
            expected_output="Around 88 units were sold in May, since the May bar sits just below 90 on the Units Sold axis.",
            retrieved_context=["Chart reference: [ATTACHMENT:sales_chart]"],
            attachments={"sales_chart": AttachmentRef(uri=CHART_URI, mime_type="image/png")},
        ),
    ]

    results = await evaluate_suites(
        suites=[
            EvalSuite(
                name="sales_chart",
                data=data,
                evaluators=[
                    CompositeEvaluator(
                        name="sales_chart",
                        metrics=[
                            GEvalCompletenessMetric(
                                name="sales_chart_completeness",
                                multimodal_rules=COMPLETENESS_RULES,
                            ),
                            GEvalGroundednessMetric(
                                name="sales_chart_groundedness",
                                multimodal_rules=GROUNDEDNESS_RULES,
                            ),
                        ],
                    )
                ],
            )
        ],
        dataset_name="multimodal_custom_rules",
    )
    print(json.dumps(results.model_dump(mode="json"), indent=2))


if __name__ == "__main__":
    asyncio.run(main())
