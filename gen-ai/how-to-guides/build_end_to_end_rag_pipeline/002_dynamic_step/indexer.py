async def main():
    state = {
        "user_query": "Give me nocturnal creatures from the dataset", # Replace with your actual query
        "use_knowledge_base": False, # Set to True to retrieve from knowledge base
        "chunks": [] # Initialize to empty list if knowledge base is disabled
    }
    config = {
        "top_k": 5,
    }
    result = await e2e_pipeline.invoke(state, config)
    print(f"Pipeline result: {result['response']}")


if __name__ == "__main__":
    asyncio.run(main())
