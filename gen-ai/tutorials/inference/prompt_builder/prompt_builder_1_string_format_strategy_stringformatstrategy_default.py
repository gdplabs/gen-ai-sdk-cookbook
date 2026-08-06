from gllm_inference.prompt_builder import PromptBuilder

prompt_builder = PromptBuilder(
    system_template="You are a {role}.",
    user_template="Tell me about {topic}."
)
messages = prompt_builder.format(role="teacher", topic="Python")
print(messages)
