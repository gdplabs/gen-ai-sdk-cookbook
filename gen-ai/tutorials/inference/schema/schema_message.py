from gllm_inference.schema import Attachment, Message

image = Attachment.from_path("path/to/chart.png")
user_msg = Message.user(["Describe this chart.", image])
