from gllm_inference.prompt_builder import PromptBuilder
from gllm_inference.schema import Message

prompt_builder = PromptBuilder(
    system_template="Talk like a {role}.",
    user_template="What is the capital city of {country}?",
)
history = [
    Message.user("Hi, there!"),
    Message.assistant("Hello!"),
]
messages = prompt_builder.format(role="pirate", country="Indonesia", history=history)
print(messages)

