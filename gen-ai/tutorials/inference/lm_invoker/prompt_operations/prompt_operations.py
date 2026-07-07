import asyncio
from gllm_inference.schema import Message

history = [
    Message.user("My name is Rina."),
    Message.assistant("Nice to meet you, Rina."),
]

output = asyncio.run(
    lm_invoker.prompt.invoke(
        history=history,
        report="What is my name?",
    )
)
print(output.text)
