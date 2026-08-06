from gllm_inference.schema import Attachment

file = Attachment.from_path('path/to/file.pdf')
uploaded_file = await lm_invoker.file.upload(file)
