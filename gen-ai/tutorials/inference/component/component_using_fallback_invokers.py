primary = build_lm_invoker(model_id="openai/gpt-5.4-nano")
backup = build_lm_invoker(model_id="openai/gpt-5.4-mini")
tertiary = build_lm_invoker(model_id="anthropic/claude-3-haiku")

for invoker in [primary, backup, tertiary]:
    invoker.prompt.build(
        system_template="You are a helpful assistant.",
        user_template="{query}",
    )

component = GenericLMComponent(
    lm_invoker=primary,
    fallback_lms=[backup, tertiary],
)
