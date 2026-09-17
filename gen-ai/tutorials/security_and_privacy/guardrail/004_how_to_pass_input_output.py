"""Show how GuardrailInput wraps input-only, output-only, and both.

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/security-and-privacy/guardrail#how-to-pass-input-andor-output-to-the-manager
"""

from gllm_guardrail import GuardrailInput


def main() -> None:
    """Build GuardrailInput variants used by GuardrailManager.check_content."""
    input_only = GuardrailInput(input="user query", output=None)
    output_only = GuardrailInput(input=None, output="model response")
    both = GuardrailInput(input="user query", output="model response")
    print(input_only)
    print(output_only)
    print(both)


if __name__ == "__main__":
    main()
