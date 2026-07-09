import asyncio
import json

from gllm_evals import AttachmentRef, EvalSuite, LLMTestCase, evaluate_suites
from gllm_evals.evaluator.composite_evaluator import CompositeEvaluator
from gllm_evals.metrics.multimodal import (
    DeepEvalImageCoherenceMetric,
    DeepEvalImageEditingMetric,
    DeepEvalImageHelpfulnessMetric,
    DeepEvalImageReferenceMetric,
    DeepEvalTextToImageMetric,
)

IMAGE_BASE_URL = (
    "https://raw.githubusercontent.com/gdplabs/gen-ai-sdk-cookbook/"
    "cd99df74b120982af30a495f1c549c5854801b46/gen-ai/tutorials/evaluations/assets/multimodal"
)
MOUNTAIN_URI = f"{IMAGE_BASE_URL}/multimodal_mountain.jpg"
FOREST_URI = f"{IMAGE_BASE_URL}/multimodal_forest.jpg"


async def main() -> None:
    # (label, metric, row) — one metric per row so each score is isolated.
    cases = [
        (
            "image_coherence",
            DeepEvalImageCoherenceMetric(),
            LLMTestCase(
                input="Write a short trip recap with photos.",
                actual_output=(
                    "We reached the summit [ATTACHMENT:mountain], then descended to the "
                    "coastal forest by the sea [ATTACHMENT:forest]."
                ),
                attachments={
                    "mountain": AttachmentRef(uri=MOUNTAIN_URI, mime_type="image/jpeg"),
                    "forest": AttachmentRef(uri=FOREST_URI, mime_type="image/jpeg"),
                },
            ),
        ),
        (
            "image_helpfulness",
            DeepEvalImageHelpfulnessMetric(),
            LLMTestCase(
                input="Explain the two landscapes with supporting photos.",
                actual_output=(
                    "The alpine zone is snow-covered [ATTACHMENT:mountain], while lower "
                    "elevations stay forested along the coast [ATTACHMENT:forest]."
                ),
                attachments={
                    "mountain": AttachmentRef(uri=MOUNTAIN_URI, mime_type="image/jpeg"),
                    "forest": AttachmentRef(uri=FOREST_URI, mime_type="image/jpeg"),
                },
            ),
        ),
        (
            "image_reference",
            DeepEvalImageReferenceMetric(),
            LLMTestCase(
                input="Describe each photo and reference it explicitly.",
                actual_output=(
                    "The first photo shows a snow-capped peak [ATTACHMENT:mountain]; the "
                    "second shows a green forest beside the sea [ATTACHMENT:forest]."
                ),
                attachments={
                    "mountain": AttachmentRef(uri=MOUNTAIN_URI, mime_type="image/jpeg"),
                    "forest": AttachmentRef(uri=FOREST_URI, mime_type="image/jpeg"),
                },
            ),
        ),
        (
            "text_to_image",
            DeepEvalTextToImageMetric(),
            LLMTestCase(
                input="A snow-capped mountain peak under a clear blue sky.",
                actual_output="[ATTACHMENT:generated]",
                attachments={"generated": AttachmentRef(uri=MOUNTAIN_URI, mime_type="image/jpeg")},
            ),
        ),
        (
            "image_editing",
            DeepEvalImageEditingMetric(),
            LLMTestCase(
                input="Original scene: [ATTACHMENT:original]. Edit: turn it into a snowy mountain.",
                actual_output="[ATTACHMENT:edited]",
                attachments={
                    "original": AttachmentRef(uri=FOREST_URI, mime_type="image/jpeg"),
                    "edited": AttachmentRef(uri=MOUNTAIN_URI, mime_type="image/jpeg"),
                },
            ),
        ),
    ]

    suites = [
        EvalSuite(name=label, data=[row], evaluators=[CompositeEvaluator(metrics=[metric], name=label)])
        for label, metric, row in cases
    ]

    result = await evaluate_suites(suites=suites, dataset_name="multimodal_native_metrics")

    print(f"Run ID: {result.run_id}")
    for suite_name, suite_result in result.suites.items():
        print(f"=== {suite_name} ===")
        print(json.dumps(suite_result.model_dump(mode="json")["results"], indent=2))


if __name__ == "__main__":
    asyncio.run(main())
