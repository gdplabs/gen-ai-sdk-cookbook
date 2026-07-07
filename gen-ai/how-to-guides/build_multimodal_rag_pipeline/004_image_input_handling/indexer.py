caption_converter = LMBasedImageToCaption.from_preset("default")

async def build_multimodal_query(state: dict[str, Any]) -> str:
    result = await caption_converter.convert(state["image_path"])
    return f"{state['user_query']}\n\n[Image context: {result.result}]"

caption_step = transform(
    operation=build_multimodal_query,
    input_map={"image_path": "image_path", "user_query": "user_query"},
    output_state="user_query",
)
