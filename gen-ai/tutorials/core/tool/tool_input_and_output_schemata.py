@tool
async def add(a: int, b: int) -> int:
    """Add two integers.

    Arguments:
        a: First addend.
        b: Second addend.
    """
    return a + b


add.input_schema   # JSON schema derived from a Pydantic model
add.output_schema  # JSON schema with a `result: int` field
