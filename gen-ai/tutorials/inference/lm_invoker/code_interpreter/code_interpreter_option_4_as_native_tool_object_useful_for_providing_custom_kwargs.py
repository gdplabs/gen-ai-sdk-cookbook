async def main() -> None:
    try:
        query = "Use the Python tool generate a histogram for the following data: [1, 1, 3, 2, 4, 1, 2]. Make it light blue."
        output = await lm_invoker.invoke(query)
        for item in output.outputs:
            print(f"=== Output item: {item.type!r} ===\n{item.output}\n")

        # Saving the created image
        for item in output.code_exec_results:
            for code_output in item.output:
                if isinstance(code_output, Attachment):
                    code_output.write_to_file("path/to/output.png")
    finally:
        await lm_invoker.release_resources()


asyncio.run(main())
