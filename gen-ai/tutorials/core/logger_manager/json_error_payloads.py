"""JSON error payloads: structured error logging in JSON mode.

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/core/logger-manager#json-error-payloads
"""

import os

from gllm_core.utils.logger_manager import LoggerManager


async def main() -> None:
    # Enable JSON mode via environment variable inside the entry point
    # so that importing this module does not mutate global process state.
    os.environ["LOG_FORMAT"] = "json"

    logger = LoggerManager().get_logger("payment_service")

    try:
        raise ValueError("Insufficient funds")
    except Exception:
        logger.error(
            "Payment failed",
            exc_info=True,
            extra={"error_code": "PAYMENT_DECLINED"},
        )


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
