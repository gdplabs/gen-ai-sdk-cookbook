"""Adding custom contextual fields to log records via `extra`.

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/core/logger-manager#adding-custom-contextual-fields
"""

from gllm_core.logging import LoggerManager


def main() -> None:
    """Log a message with request-scoped contextual fields."""
    logger = LoggerManager().get_logger("payment_service")

    logger.info(
        "Request processed",
        extra={
            "request_id": "req-abc-123",
            "user_id": "usr-456",
        },
    )


if __name__ == "__main__":
    main()
