from contextvars import ContextVar

from gllm_core.logging import LoggerManager


request_id = ContextVar("request_id", default=None)

manager = LoggerManager()
manager.register_global_json_field("service", lambda: "payment-service")
manager.register_global_json_field("request_id", request_id.get)

request_id.set("req-abc-123")
manager.get_logger("payment_service").info("Request processed")
