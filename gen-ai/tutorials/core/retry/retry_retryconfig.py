from gllm_core.retry import RetryConfig

config = RetryConfig(
    max_retries=3,           # Up to 3 retries (4 total attempts)
    base_delay=1.0,          # Initial delay in seconds
    max_delay=30.0,          # Cap on each delay
    jitter=True,             # Add random jitter (0-25%)
    timeout=60.0,            # Overall timeout for all attempts
    retry_on_exceptions=(Exception,),  # Which exceptions trigger retry
    non_retryable_exceptions=(TimeoutError,),  # Never retry these
)
