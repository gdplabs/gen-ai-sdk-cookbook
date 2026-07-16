"""JSON error payloads: structured error logging in JSON mode.

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/core/logger-manager#json-error-payloads
"""

import os

from gllm_core.utils.logger_manager import LoggerManager

# Enable JSON mode via environment variable
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
