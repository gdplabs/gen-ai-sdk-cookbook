import logging
from gllm_core.utils.logger_manager import LoggerManager


manager = LoggerManager()
file_handler = logging.FileHandler("app.log")

manager.add_handler(file_handler)
logger = manager.get_logger("gllm_core.my_component")

logger.info("This will go to both the console and app.log")
