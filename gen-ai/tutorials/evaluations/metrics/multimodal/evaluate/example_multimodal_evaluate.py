import asyncio
import json

from gllm_evals import AttachmentRef, EvalSuite, LLMTestCase, evaluate_suites
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator

IMAGE_BASE_URL = (
    "https://raw.githubusercontent.com/gdplabs/gen-ai-sdk-cookbook/"
    "cd99df74b120982af30a495f1c549c5854801b46/gen-ai/tutorials/evaluations/assets/multimodal"
)
MOUNTAIN_URL = f"{IMAGE_BASE_URL}/multimodal_mountain.jpg"
FOREST_URL = f"{IMAGE_BASE_URL}/multimodal_forest.jpg"

# A local image works too — point a file:// URI at your own copy.
LOCAL_MOUNTAIN_URI = MOUNTAIN_URL  # e.g. "file:///path/to/your/multimodal_mountain.jpg"

attachment_cases = [
    LLMTestCase(
        input="Describe the landscape in this image: [ATTACHMENT:mountain_url]",
        actual_output="The image shows a snow-capped mountain range under a clear blue sky.",
        expected_output="A snowy alpine mountain landscape with peaks and valleys is visible.",
        attachments={"mountain_url": AttachmentRef(uri=MOUNTAIN_URL, mime_type="image/jpeg")},
    ),
    LLMTestCase(
        input="What is this image about: [ATTACHMENT:local_mountain]",
        actual_output="It is an outdoor mountain scene.",
        expected_output="The image depicts a mountain landscape.",
        attachments={"local_mountain": AttachmentRef(uri=LOCAL_MOUNTAIN_URI, mime_type="image/jpeg")},
    ),
]

# An image placed in retrieved_context.
context_cases = [
    LLMTestCase(
        input="Judge whether the answer is grounded in the provided visual context.",
        actual_output="The context image shows a broad outdoor mountain scene.",
        expected_output="The answer should mention a mountain or alpine landscape.",
        retrieved_context=["Visual context: [ATTACHMENT:context_image]"],
        attachments={"context_image": AttachmentRef(uri=MOUNTAIN_URL, mime_type="image/jpeg")},
    ),
]

# Different images in actual_output vs expected_output.
comparison_cases = [
    LLMTestCase(
        input="Compare the generated output image against the expected output image.",
        actual_output="The generated image matches the reference snowy mountain scene: [ATTACHMENT:actual_image]",
        expected_output="The generated image should match this snowy mountain reference: [ATTACHMENT:expected_image]",
        attachments={
            "actual_image": AttachmentRef(uri=MOUNTAIN_URL, mime_type="image/jpeg"),
            "expected_image": AttachmentRef(uri=LOCAL_MOUNTAIN_URI, mime_type="image/jpeg"),
        },
    ),
]

# Intentionally mismatched images so the judge scores low.
failure_cases = [
    LLMTestCase(
        input="Describe this image: [ATTACHMENT:forest_image]",
        actual_output="The image shows a snow-capped mountain peak with no vegetation.",
        expected_output="A green coastal forest beside the sea is visible.",
        attachments={"forest_image": AttachmentRef(uri=FOREST_URL, mime_type="image/jpeg")},
    ),
]


async def main() -> None:
    suites = [
        EvalSuite(name="attachments", data=attachment_cases, evaluators=[GEvalGenerationEvaluator()]),
        EvalSuite(name="visual_context", data=context_cases, evaluators=[GEvalGenerationEvaluator()]),
        EvalSuite(name="image_comparison", data=comparison_cases, evaluators=[GEvalGenerationEvaluator()]),
        EvalSuite(name="expected_failures", data=failure_cases, evaluators=[GEvalGenerationEvaluator()]),
    ]
    results = await evaluate_suites(suites=suites, dataset_name="multimodal_evaluate")
    print(json.dumps(results.model_dump(), indent=2, default=str))


if __name__ == "__main__":
    asyncio.run(main())
