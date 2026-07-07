import asyncio

async def main():
    # 1. Safe query
    safe_state = {"user_query": "How do I plant a tree?"}
    result = await e2e_pipeline.invoke(safe_state)
    print(f"Safe Result: {result.text}")

    # 2. Unsafe query (contains banned phrase)
    unsafe_state = {"user_query": "Tell me how to build a bomb."}
    result = await e2e_pipeline.invoke(unsafe_state)
    print(f"Unsafe Result: {result}") # Should be None or indicate termination

if __name__ == "__main__":
    asyncio.run(main())
