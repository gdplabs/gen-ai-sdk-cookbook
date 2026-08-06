async def main() -> None:
    try:
        query = """
        List all transport protocols supported by the 2025-03-26 version of
        the MCP spec (modelcontextprotocol/modelcontextprotocol) in bullet points"
        """
        output = await lm_invoker.invoke(query)
        for item in output.outputs:
            print(f"=== Output item: {item.type!r} ===\n{item.output}\n")
    finally:
        await lm_invoker.release_resources()


asyncio.run(main())
