from gllm_inference.output_transformer import OutputTransformerConfig

output_transformers = [
    OutputTransformerConfig.validation({"structured", "text"}, mode="any"),
]
