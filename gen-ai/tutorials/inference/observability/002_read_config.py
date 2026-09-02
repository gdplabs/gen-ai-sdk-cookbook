"""Read back the current process-wide trace content capture policy.

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/inference/observability#reading-the-current-configuration
"""

from gllm_inference.observability import get_lm_trace_content_config


def main() -> None:
    """Print a couple of fields from the immutable current-config snapshot."""
    current = get_lm_trace_content_config()
    print(current.input_text, current.output_text)


if __name__ == "__main__":
    main()
