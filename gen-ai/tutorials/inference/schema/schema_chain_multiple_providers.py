from gllm_inference.schema import Attachment, Message

attachment = Attachment.from_path("path/to/image.png").configure_context(
    fields=["filename", "mime_type"],
)

contents = attachment.to_context_contents()
message = Message.user(["Describe this image.", *contents])
