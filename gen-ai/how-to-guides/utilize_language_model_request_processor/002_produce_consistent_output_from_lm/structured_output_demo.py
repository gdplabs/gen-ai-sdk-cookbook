"""Runnable example for producing consistent structured output from an LM."""

import asyncio
import logging

from pydantic import BaseModel

from gllm_inference.lm_invoker.lm_invoker import BaseLMInvoker
from gllm_inference.prompt_builder import PromptBuilder
from gllm_inference.request_processor import LMRequestProcessor
from gllm_inference.schema import LMOutput, Message, ModelId


class CreatureDecision(BaseModel):
    creature: str
    habitat: str
    confidence: float
    reasoning: str


class StructuredOutputDemoInvoker(BaseLMInvoker):
    async def _invoke(self, messages, config, transformer, stream) -> LMOutput:
        del config, transformer, stream
        prompt = " ".join(str(content) for message in messages for content in message.contents)

        if "forest" in prompt.lower():
            payload = {
                "creature": "Luminafox",
                "habitat": "moonlit forest",
                "confidence": 0.98,
                "reasoning": "The prompt asks for a forest creature with glowing fur.",
            }
        else:
            payload = {
                "creature": "Dusk Panther",
                "habitat": "twilight plains",
                "confidence": 0.93,
                "reasoning": "The prompt focuses on a stealth hunter rather than a glowing animal.",
            }

        output = LMOutput()
        if self.response_schema:
            output.add_structured(self._extract_structured_output(payload))
        else:
            output.add_text(f"{payload['creature']} from {payload['habitat']}")
        return output

    def _format_messages(self, messages: list[Message]) -> list[Message]:
        return messages


async def main() -> None:
    logging.disable(logging.CRITICAL)

    invoker = StructuredOutputDemoInvoker(model_id=ModelId.from_string("openai/gpt-5-nano"))
    processor = LMRequestProcessor(
        PromptBuilder(
            system_template="Always return the requested creature decision.",
            user_template="{query}",
        ),
        invoker,
    )
    processor.set_response_schema(CreatureDecision)

    forest_result = await processor.process(query="Pick the best creature for a glowing forest mascot.")
    stealth_result = await processor.process(query="Pick the best creature for a stealth-themed sentinel.")

    print("Forest mascot decision")
    print(forest_result.structured_output.model_dump_json(indent=2))
    print("Stealth sentinel decision")
    print(stealth_result.structured_output.model_dump_json(indent=2))


if __name__ == "__main__":
    asyncio.run(main())
