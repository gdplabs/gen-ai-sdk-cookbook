summarizer = SummarizerComponent.from_config(
    model_id="openai/gpt-5.4-nano",
)

result = asyncio.run(summarizer.run(
    text="The quick brown fox jumps over the lazy dog.",
    style="poetic",
))
print(result)
