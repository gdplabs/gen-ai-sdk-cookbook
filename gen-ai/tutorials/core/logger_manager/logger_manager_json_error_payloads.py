logger = LoggerManager().get_logger("payment_service")

try:
    process_payment()
except Exception:
    logger.error(
        "Payment failed",
        exc_info=True,
        extra={"error_code": "PAYMENT_DECLINED"},
    )
