class MyComponent(Base, LMComponent):
    # TODO: Remove lm_request_processor in v0.7.0. Use lm_invoker instead.
    def __init__(
        self,
        lm_request_processor: LMRequestProcessor | None = None,
        *,
        lm_invoker: BaseLMInvoker | None = None,
        fallback_lms: list[BaseLMInvoker] | None = None,
    ) -> None:
        if (lm_request_processor is None) == (lm_invoker is None):
            raise ValueError("Provide exactly one of lm_request_processor or lm_invoker.")

        if lm_request_processor is not None:
            lm_invoker = lm_request_processor.to_lm_invoker_cascade()

        Base.__init__(self)
        LMComponent.__init__(self, lm_invoker=lm_invoker, fallback_lms=fallback_lms)
