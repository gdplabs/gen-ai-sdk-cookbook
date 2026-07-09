import asyncio

from gllm_evals import AttachmentRef, LLMTestCase
from gllm_evals.metrics.multimodal import DeepEvalImageEditingMetric

IMAGE_BASE_URL = (
    "https://raw.githubusercontent.com/gdplabs/gen-ai-sdk-cookbook/"
    "cd99df74b120982af30a495f1c549c5854801b46/gen-ai/tutorials/evaluations/assets/multimodal"
)
# The forest is the original; the mountain stands in for the edited result.
ORIGINAL_IMAGE_URL = f"{IMAGE_BASE_URL}/multimodal_forest.jpg"
EDITED_IMAGE_URL = f"{IMAGE_BASE_URL}/multimodal_mountain.jpg"


async def main():
    metric = DeepEvalImageEditingMetric()
    data = LLMTestCase(
        input="Original scene: [ATTACHMENT:original]. Edit: turn it into a snowy mountain.",
        actual_output="[ATTACHMENT:edited]",
        attachments={
            "original": AttachmentRef(uri=ORIGINAL_IMAGE_URL, mime_type="image/jpeg"),
            "edited": AttachmentRef(uri=EDITED_IMAGE_URL, mime_type="image/jpeg"),
        },
    )
    result = await metric.evaluate(data)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
