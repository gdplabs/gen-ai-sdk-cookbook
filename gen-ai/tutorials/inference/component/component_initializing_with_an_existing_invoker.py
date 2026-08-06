from gllm_inference.lm_invoker import build_lm_invoker

invoker = build_lm_invoker(model_id="openai/gpt-5.4-nano")
invoker = invoker.prompt.build(
    system_template="You are a summarization expert.",
    user_template="Summarize the following text in a {style} style:\n\n{text}",
)

summarizer = SummarizerComponent(lm_invoker=invoker)
result = asyncio.run(summarizer.run(
    text="The quick brown fox jumps over the lazy dog.",
    style="poetic",
))
