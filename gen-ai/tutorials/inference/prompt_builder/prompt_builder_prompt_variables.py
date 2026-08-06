from gllm_inference.prompt_builder import PromptBuilder

prompt_builder = PromptBuilder(
    system_template="Talk like a {role}.",
    user_template="What is the capital city of {country}?",
)
messages = prompt_builder.format(role="pirate", country="Indonesia")
print(messages)
