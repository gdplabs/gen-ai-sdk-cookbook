"""Configure GuardrailManager to propagate selected exception types.

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/security-and-privacy/guardrail#exception-propagation-raiseonexceptions
"""

import asyncio

from gllm_guardrail import GuardrailManager, PhraseMatcherEngine


async def main() -> None:
    """Instantiate a manager that propagates TimeoutError and ConnectionError."""
    guardrail = GuardrailManager(
        engine=PhraseMatcherEngine(),
        raise_on_exceptions=(TimeoutError, ConnectionError),
    )

    result = await guardrail.check_content("This is a safe message.")
    print(result.is_safe, result.reason)


if __name__ == "__main__":
    asyncio.run(main())
