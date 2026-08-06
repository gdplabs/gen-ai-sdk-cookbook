from gllm_inference.component import LMComponent
from gllm_core.schema import main


class SummarizerComponent(LMComponent):
    prompt_vars = {"text", "style"}
    default_system_template = "You are a summarization expert."
    default_user_template = "Summarize the following text in a {style} style:\n\n{text}"

    @main
    async def summarize(self, text: str, style: str) -> str:
        output = await self._invoke_lm(text=text, style=style)
        return output.text
