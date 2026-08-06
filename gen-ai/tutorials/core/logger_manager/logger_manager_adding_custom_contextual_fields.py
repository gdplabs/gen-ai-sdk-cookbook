from gllm_core.utils.logger_manager import LoggerManager


logger = LoggerManager().get_logger("payment_service")

logger.info("Request processed", extra={
    "request_id": "req-abc-123",
    "user_id": "usr-456",
})
