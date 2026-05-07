import asyncio

from dotenv import load_dotenv
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM

load_dotenv()


async def main():
    lm_invoker = OpenAILMInvoker(OpenAILM.GPT_5_NANO)
    lm_invoker.prompt.build(
        system_template="You are a helpful coding assistant.",
        user_template="Summarize this bug report in 3 bullets: {report}",
    )

    output = await lm_invoker.prompt.invoke(
        report="Summarize why retries are useful for API calls.",
    )
    print(output.text)


if __name__ == "__main__":
    asyncio.run(main())
