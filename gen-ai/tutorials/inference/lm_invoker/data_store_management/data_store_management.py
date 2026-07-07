from gllm_inference.schema import NativeTool, NativeToolType

# Option 1: as dictionary
data_store_tool = {"type": "data_store", "data_stores": [store], **kwargs}
# Option 2: as native tool object
data_store_tool = NativeTool.data_store(data_stores=[store], **kwargs)

lm_invoker.set_tools([data_store_tool])
