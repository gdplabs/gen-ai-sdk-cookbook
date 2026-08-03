"""Global JSON fields: attaching context to every JSON log record.

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/core/logger-manager#adding-global-json-fields
"""

import os
from contextvars import ContextVar

from gllm_core.utils.logger_manager import LoggerManager

request_id: ContextVar[str | None] = ContextVar("request_id", default=None)


async def main() -> None:
    # Enable JSON mode via environment variable inside the entry point
    # so that importing this module does not mutate global process state.
    os.environ["LOG_FORMAT"] = "json"

    manager = LoggerManager()
    manager.register_global_json_field("service", lambda: "payment-service")
    manager.register_global_json_field("request_id", request_id.get)

    request_id.set("req-abc-123")
    manager.get_logger("payment_service").info("Request processed")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
