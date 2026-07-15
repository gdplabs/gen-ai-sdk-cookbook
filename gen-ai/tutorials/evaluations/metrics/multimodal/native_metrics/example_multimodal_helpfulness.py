import asyncio

from gllm_evals import AttachmentRef, LLMTestCase
from gllm_evals.metrics.multimodal import DeepEvalImageHelpfulnessMetric

IMAGE_BASE_URL = (
    "https://raw.githubusercontent.com/gdplabs/gen-ai-sdk-cookbook/"
    "cd99df74b120982af30a495f1c549c5854801b46/gen-ai/tutorials/evaluations/assets/multimodal"
)
MOUNTAIN_URL = f"{IMAGE_BASE_URL}/multimodal_mountain.jpg"
FOREST_URL = f"{IMAGE_BASE_URL}/multimodal_forest.jpg"


async def main():
    metric = DeepEvalImageHelpfulnessMetric()
    data = LLMTestCase(
        input="Explain the two landscapes with supporting photos.",
        actual_output=(
            "The alpine zone is snow-covered [ATTACHMENT:mountain], while lower "
            "elevations stay forested along the coast [ATTACHMENT:forest]."
        ),
        attachments={
            "mountain": AttachmentRef(uri=MOUNTAIN_URL, mime_type="image/jpeg"),
            "forest": AttachmentRef(uri=FOREST_URL, mime_type="image/jpeg"),
        },
    )
    result = await metric.evaluate(data)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
