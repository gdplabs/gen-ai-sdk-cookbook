import asyncio

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


async def main() -> None:
    prompt_builder = PromptBuilder(user_template="Summarize this in a {style} style: {text}")
    lm_invoker = OpenAILMInvoker(OpenAILM.GPT_5_NANO)
    try:
        # Use `from_lm_components` when you already have a prompt builder and LM invoker.
        summarizer = LMBasedSummarizer.from_lm_components(
            prompt_builder,
            lm_invoker,
            style="brief",
        )

        # Use `from_lm_request_processor` when you want to reuse an already-configured LMRP.
        lm_request_processor = LMRequestProcessor(prompt_builder, lm_invoker)
        summarizer = LMBasedSummarizer.from_lm_request_processor(
            lm_request_processor,
            style="brief",
        )

        # Both helper constructors also accept `fallback_lmrp`, an ordered list of fallback
        # processors tried in order if the primary fails with an invoker error or timeout.
        primary_lmrp = LMRequestProcessor(prompt_builder, lm_invoker)
        fallback_lmrp = LMRequestProcessor(prompt_builder, lm_invoker)
        summarizer = LMBasedSummarizer.from_lm_request_processor(
            primary_lmrp,
            fallback_lmrp=[fallback_lmrp],
            style="brief",
        )

        output = await summarizer.summarize("Retries improve reliability by re-attempting failed API calls.")
        print(f"Response: {output}")
    finally:
        await lm_invoker.release_resources()


if __name__ == "__main__":
    asyncio.run(main())
