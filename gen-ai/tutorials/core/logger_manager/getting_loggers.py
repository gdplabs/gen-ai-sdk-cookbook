"""Getting loggers: root logger and named child loggers.

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/core/logger-manager#getting-loggers
"""

from gllm_core.utils.logger_manager import LoggerManager

manager = LoggerManager()

# 1. Root logger
root_logger = manager.get_logger()

# 2. Child logger for a specific module or component
component_logger = manager.get_logger("gllm_core.my_component")

root_logger.info("Root logger message")
component_logger.info("Component logger message")
