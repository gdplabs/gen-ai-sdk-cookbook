"""A quickstart example for using LoggerManager.

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/core/logger-manager
"""

import logging

from gllm_core.utils.logger_manager import LoggerManager


manager = LoggerManager()
logger = manager.get_logger("my_app")

logger.info("Application started")
logger.debug("Debug details", extra={"error_code": "SAMPLE"})