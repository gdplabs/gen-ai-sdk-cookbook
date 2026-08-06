from gllm_inference.schema import Attachment

file = Attachment.from_path('path/to/file.pdf')
await lm_invoker.data_store.add_file(store, file)
