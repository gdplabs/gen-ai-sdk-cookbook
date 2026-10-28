import asyncio
import os

from gllm_evals import AttachmentRef, LLMTestCase
from gllm_evals.metrics.multimodal import DeepEvalTextToImageMetric
from gllm_inference.lm_invoker import build_lm_invoker

IMAGE_BASE_URL = (
    "https://raw.githubusercontent.com/gdplabs/gen-ai-sdk-cookbook/"
    "cd99df74b120982af30a495f1c549c5854801b46/gen-ai/tutorials/evaluations/assets/multimodal"
)
# The mountain image stands in for your text-to-image system's output.
GENERATED_IMAGE_URL = f"{IMAGE_BASE_URL}/multimodal_mountain.jpg"


async def main():
    metric = DeepEvalTextToImageMetric(
        models=build_lm_invoker(
            model_id="openrouter/deepseek/deepseek-v4.1-flash-1017",
            credentials=os.getenv("OPENROUTER_API_KEY"),
            config={"provider": {"order": ["inference.net"], "allow_fallbacks": False}},
        )
    )
    data = LLMTestCase(
        input="A snow-capped mountain peak under a clear blue sky.",
        actual_output="[ATTACHMENT:generated]",
        attachments={
            "generated": AttachmentRef(uri=GENERATED_IMAGE_URL, mime_type="image/jpeg"),
        },
    )
    result = await metric.evaluate(data)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
