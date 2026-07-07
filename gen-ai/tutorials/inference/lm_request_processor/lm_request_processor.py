from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM
from gllm_inference.prompt_builder import PromptBuilder
from gllm_inference.request_processor import LMRequestProcessor, UsesLM


class LMBasedSummarizer(UsesLM):
    def __init__(self, lm_request_processor: LMRequestProcessor, style: str = "concise"):
        self.lm_request_processor = lm_request_processor
        self.style = style

    async def summarize(self, text: str) -> str:
        output = await self.lm_request_processor.process(text=text, style=self.style)
        return output.text


prompt_builder = PromptBuilder(user_template="Summarize this in a {style} style: {text}")
lm_invoker = OpenAILMInvoker(OpenAILM.GPT_5_NANO)

summarizer = LMBasedSummarizer.from_lm_components(
    prompt_builder,
    lm_invoker,
    style="brief",
)
