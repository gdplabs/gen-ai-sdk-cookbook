async def main() -> None:
    try:
        query = "How much did `Zootopia 2` make in the box office?"
        output = await lm_invoker.invoke(query)
        for item in output.outputs:
            print(f"=== Output item: {item.type!r} ===\n{item.output}\n")
    finally:
        await lm_invoker.release_resources()


asyncio.run(main())
