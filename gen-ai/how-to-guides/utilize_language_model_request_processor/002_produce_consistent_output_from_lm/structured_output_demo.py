"""Runnable example for producing consistent structured output from LM."""

import asyncio

from dotenv import load_dotenv
from pydantic import BaseModel

from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.prompt_builder import PromptBuilder
from gllm_inference.request_processor import LMRequestProcessor


load_dotenv()


class CreatureDecision(BaseModel):
    creature: str
    habitat: str
    confidence: float
    reasoning: str


async def main() -> None:
    lm_invoker = OpenAILMInvoker(
        model_name="gpt-4o-mini",
        response_schema=CreatureDecision,
    )

    prompt_builder = PromptBuilder(
        system_template="Always return the creature decision.",
        user_template="{query}",
    )

    processor = LMRequestProcessor(prompt_builder, lm_invoker)

    forest_result = await processor.process(query="Pick the best creature for a forest mascot.")

    print("Forest mascot decision")
    print(forest_result.structured_output.model_dump_json(indent=2))


if __name__ == "__main__":
    asyncio.run(main())