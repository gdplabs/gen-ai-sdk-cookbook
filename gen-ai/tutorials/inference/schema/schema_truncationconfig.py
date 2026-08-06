from gllm_inference.schema.config import TruncationConfig, TruncateSide

config = TruncationConfig(
    max_length=1000,
    truncate_side=TruncateSide.RIGHT  # keep the start, truncate the end (default)
)
