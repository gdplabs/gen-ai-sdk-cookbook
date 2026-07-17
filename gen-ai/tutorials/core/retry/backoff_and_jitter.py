"""Exponential backoff and jitter configuration.

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/core/retry#exponential-backoff-and-jitter
"""

from gllm_core.retry import RetryConfig


def main():
    # Exponential backoff with no jitter — predictable delays
    no_jitter = RetryConfig(
        max_retries=3,
        base_delay=1.0,
        max_delay=10.0,
        jitter=False,  # Exact delays: 1s, 2s, 4s
    )
    print(
        f"No jitter config: max_retries={no_jitter.max_retries}, "
        f"base_delay={no_jitter.base_delay}"
    )
    print("Expected delays without jitter: 1s, 2s, 4s")

    # With jitter enabled (default), delays become:
    # Attempt 1: ~1.0-1.25s
    # Attempt 2: ~2.0-2.5s
    # Attempt 3: ~4.0-5.0s (capped at max_delay)
    with_jitter = RetryConfig(
        max_retries=3,
        base_delay=1.0,
        max_delay=10.0,
        jitter=True,
    )
    print(
        f"With jitter config: max_retries={with_jitter.max_retries}, "
        f"jitter={with_jitter.jitter}"
    )
    print("Expected delays with jitter: ~1.0-1.25s, ~2.0-2.5s, ~4.0-5.0s")


if __name__ == "__main__":
    main()
