"""Configuring log levels and formats.

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/core/logger-manager#configuring-levels-and-formats
"""

import logging

from gllm_core.utils.logger_manager import LoggerManager

manager = LoggerManager()

# Set log level for the entire hierarchy
manager.set_level(logging.DEBUG)

# Set a custom log format string
manager.set_log_format("[%(asctime)s %(name)s %(levelname)s] %(message)s")

# Set a custom date format
manager.set_date_format("%Y-%m-%d %H:%M:%S")

logger = manager.get_logger("my_app")
logger.debug("Debug message with custom format")
