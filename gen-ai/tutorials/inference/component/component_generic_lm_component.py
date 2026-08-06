component = GenericLMComponent.from_config(
    model_id="openai/gpt-5.4-nano",
    system_template="Talk like a {role}.",
)

output = asyncio.run(component.run(query="What is the capital of France?", role="pirate"))
print(output.text)
