"""Opt in to (and back out of) process-wide LM trace content capture.

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/inference/observability#configuring-trace-content-capture
"""

from gllm_inference.observability import (
    LMTraceContentConfig,
    configure_lm_trace_content,
    get_lm_trace_content_config,
)


def main() -> None:
    """Enable trace content capture, inspect the policy, then restore the default."""
    configure_lm_trace_content(
        LMTraceContentConfig(
            system_instructions=True,
            tool_definitions=True,
            input_text=True,
            output_text=True,
            output_thinking=True,
        )
    )
    print("after opt-in:", get_lm_trace_content_config().input_text)

    configure_lm_trace_content(None)  # disable trace content capture
    print("after disable:", get_lm_trace_content_config().input_text)


if __name__ == "__main__":
    main()
