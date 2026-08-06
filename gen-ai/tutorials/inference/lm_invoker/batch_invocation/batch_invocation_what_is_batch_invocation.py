import asyncio
from gllm_core.retry import RetryConfig
from gllm_inference.lm_invoker import AnthropicLMInvoker
from gllm_inference.model import AnthropicLM

lm_invoker = AnthropicLMInvoker(AnthropicLM.CLAUDE_SONNET_4_6, retry_config=RetryConfig(timeout=360))

requests = {
    f"request_{letter}": f"Name an animal that starts with the letter '{letter}'"
    for letter in "ABCDE"
}

async def main():
    try:
        results = await lm_invoker.batch.invoke(requests)

        print("Results:")
        for result_id, result in results.items():
            print(f">> {result_id}: {result.text}")
    finally:
        await lm_invoker.release_resources()

if __name__ == "__main__":
    asyncio.run(main())
