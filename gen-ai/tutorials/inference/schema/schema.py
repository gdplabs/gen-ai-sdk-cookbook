from gllm_inference.schema import Attachment

# From a local file path
attachment = Attachment.from_path("path/to/image.jpeg")

# From a remote URL (downloads the file)
attachment = Attachment.from_url("https://example.com/image.png")

# From a data URL
attachment = Attachment.from_data_url("data:image/jpeg;base64,<base64_encoded_image>")

# From raw bytes
attachment = Attachment.from_bytes(b"<file_bytes>")
