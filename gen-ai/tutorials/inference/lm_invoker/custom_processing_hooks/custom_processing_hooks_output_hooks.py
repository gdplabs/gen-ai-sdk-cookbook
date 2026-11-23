import asyncio

from gllm_inference.lm_invoker import OpenAILMInvoker


def collect_citations(item, output):
    if not getattr(output, "citations", None):
        return

    print(f"current citations: {len(output.citations)}")


async def main() -> None:
    lm_invoker = OpenAILMInvoker(
        model_name="gpt-5-nano",
        output_hooks=[collect_citations],
    )
    result = await lm_invoker.invoke("Summarize the result and cite sources.")
    print(result.text)


if __name__ == "__main__":
    asyncio.run(main())
