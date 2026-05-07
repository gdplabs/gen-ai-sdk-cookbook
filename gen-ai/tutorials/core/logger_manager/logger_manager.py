import logging
from gllm_core.utils.logger_manager import LoggerManager


manager = LoggerManager()
logger = manager.get_logger("my_app")

logger.info("Application started")
logger.debug("Debug details", extra={"error_code": "SAMPLE"})

print("\n--- Changing log level to DEBUG ---")
manager.set_level(logging.DEBUG)
logger.debug("Now debug messages are visible")
