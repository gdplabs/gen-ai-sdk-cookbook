from gllm_pipeline.steps._func import transform
from gllm_pipeline.steps.step_error_handler import RaiseStepErrorHandler

def may_fail(data: dict) -> str:
    if not data.get("valid"):
        raise ValueError("Invalid input")
    return data["text"].upper()

# By default, errors will be raised with context
step = transform(
    may_fail,
    input_map=["text", "valid"],
    output_state="result",
    # error_handler=RaiseStepErrorHandler()  # 👈 This is the default
)
