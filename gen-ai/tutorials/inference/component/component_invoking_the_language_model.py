output = await self._invoke_lm(
    history=[Message.user("Hello")],
    extra_contents=[attachment],
    hyperparameters={"temperature": 0.7},
    event_emitter=emitter,
    max_calls=3,
    **prompt_kwargs,
)
