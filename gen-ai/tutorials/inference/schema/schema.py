import asyncio
from gllm_inference.schema import Attachment

async def load_attachment_async():
    # From a local file path (async)
    attachment = await Attachment.aio.from_path("path/to/image.jpeg")

    # From a remote URL (async, downloads the file)
    attachment = await Attachment.aio.from_url("https://example.com/image.png")

    # From a data URL (async)
    attachment = await Attachment.aio.from_data_url("data:image/jpeg;base64,<base64_encoded_image>")

    # From raw bytes (async)
    attachment = await Attachment.aio.from_bytes(b"<file_bytes>")

    return attachment

# Run the async function
attachment = asyncio.run(load_attachment_async())
