from gllm_inference.prompt_builder import PromptBuilder

prompt_builder = PromptBuilder(
    system_template="Talk like a pirate.",
    user_template="What is the capital city of Indonesia?",
)
messages = prompt_builder.format()
print(messages)
