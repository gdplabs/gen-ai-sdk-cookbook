from gllm_inference.prompt_builder import PromptBuilder
from gllm_inference.schema import Attachment

image = Attachment.from_path("path/to/image.png")

prompt_builder = PromptBuilder(
    system_template="Talk like a {role}.",
    user_template="What is the capital city of {country}?",
)
messages = prompt_builder.format(
    role="pirate",
    country="Indonesia",
    extra_contents=[image],
)
print(messages)

