from gllm_inference.prompt_builder import PromptBuilder
from gllm_inference.schema import Message


def quickstart_example():
    prompt_builder = PromptBuilder(
        system_template="Talk like a pirate.",
        user_template="What is the capital city of Indonesia?",
    )
    messages = prompt_builder.format()
    print("=== Quickstart ===")
    print(messages)


def prompt_variables_example():
    prompt_builder = PromptBuilder(
        system_template="Talk like a {role}.",
        user_template="What is the capital city of {country}?",
    )
    messages = prompt_builder.format(role="pirate", country="Indonesia")
    print("\n=== Prompt Variables ===")
    print(messages)


def history_example():
    prompt_builder = PromptBuilder(
        system_template="Talk like a {role}.",
        user_template="What is the capital city of {country}?",
    )
    history = [
        Message.user("Hi, there!"),
        Message.assistant("Hello!"),
    ]
    messages = prompt_builder.format(role="pirate", country="Indonesia", history=history)
    print("\n=== With History ===")
    print(messages)


if __name__ == "__main__":
    quickstart_example()
    prompt_variables_example()
    history_example()
