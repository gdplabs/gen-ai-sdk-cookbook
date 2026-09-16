"""Configure stream buffer limits on GuardrailManager.

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/security-and-privacy/guardrail#stream-buffer-limits
"""

from gllm_guardrail import GuardrailManager, PhraseMatcherEngine


def main() -> None:
    """Instantiate a manager with custom stream buffer caps."""
    guardrail = GuardrailManager(
        engine=PhraseMatcherEngine(),
        max_stream_buffer_bytes=512_000,
        max_stream_buffer_chunks=5_000,
    )
    print(guardrail)


if __name__ == "__main__":
    main()
