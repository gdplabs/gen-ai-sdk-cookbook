import asyncio

from gllm_inference.lm_invoker import GoogleLMInvoker


async def main() -> None:
    lm_invoker = GoogleLMInvoker("gemini-3.1-flash-lite-preview")

    files = await lm_invoker.file.list()

    if not files:
        print("No files found.")

    for file in files:
        print(f" - {file}")


if __name__ == "__main__":
    asyncio.run(main())
