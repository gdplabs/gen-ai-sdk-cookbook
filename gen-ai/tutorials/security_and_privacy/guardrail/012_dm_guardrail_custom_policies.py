"""Configure the decision-model guardrail with a local policy and threshold.

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/security-and-privacy/guardrail#policy-based-decision-model-checks-default-engine
"""

import asyncio
from pathlib import Path

from dotenv import load_dotenv
from gllm_guardrail import DMGuardrailEngine, DMGuardrailEngineConfig, GuardrailManager


async def main() -> None:
    """Check content against a custom policy with a higher threshold."""
    load_dotenv()
    engine = DMGuardrailEngine.from_config(
        model_id="openrouter/typesafe/jev-1.13",
        engine_config=DMGuardrailEngineConfig(
            policy_config_path=str(Path(__file__).with_name("my_policies.yaml")),
            default_threshold=0.7,
        ),
    )
    guardrail = GuardrailManager(engine=engine)
    try:
        result = await guardrail.check_content("Please share a secret password.")
        print(result.is_safe, result.reason)
        print(result.category, result.policy, result.score)
    finally:
        await engine.dm_invoker.release_resources()


if __name__ == "__main__":
    asyncio.run(main())
