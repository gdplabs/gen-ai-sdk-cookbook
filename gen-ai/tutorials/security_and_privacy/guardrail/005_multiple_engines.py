"""Run multiple guardrail engines with GuardrailManager.

This example combines a lightweight PhraseMatcherEngine with an LLM-backed
NemoGuardrailEngine, so it requires an OpenAI API key.

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/security-and-privacy/guardrail#multiple-engines-example
"""

import asyncio
import os

from dotenv import load_dotenv
from gllm_inference.lm_invoker import build_lm_invoker
from gllm_guardrail import GuardrailManager, NemoGuardrailEngine, PhraseMatcherEngine
from gllm_guardrail.config.safety import ContentSafetyConfigBuilder
from gllm_guardrail.engine.nemo_engine import NemoGuardrailEngineConfig

load_dotenv()


async def main() -> None:
    """Run sequential phrase-matcher and NeMo guardrail engines."""
    phrase_engine = PhraseMatcherEngine(banned_phrases=["sk-"])

    invoker = build_lm_invoker(
        model_id="openai/gpt-4o-mini",
        credentials=os.environ["OPENAI_API_KEY"],
    )
    nemo_engine = NemoGuardrailEngine(
        config=NemoGuardrailEngineConfig(
            lm_invoker=invoker,
            content_safety_config=ContentSafetyConfigBuilder(),
        )
    )

    guardrail = GuardrailManager(engine=[phrase_engine, nemo_engine])
    result = await guardrail.check_content("Check this content.")
    print(result.is_safe, result.reason)


if __name__ == "__main__":
    asyncio.run(main())
