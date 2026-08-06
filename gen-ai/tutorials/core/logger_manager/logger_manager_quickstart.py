from gllm_core.utils.logger_manager import LoggerManager


manager = LoggerManager()
logger = manager.get_logger("my_app")

logger.info("Application started")
logger.debug("Debug details", extra={"error_code": "SAMPLE"})
