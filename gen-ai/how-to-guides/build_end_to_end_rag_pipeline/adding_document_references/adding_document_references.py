from gllm_generation.reference_formatter import SimilarityBasedReferenceFormatter
from gllm_pipeline.steps import step

reference_formatter = SimilarityBasedReferenceFormatter(
    em_invoker=em_invoker, threshold=0.5, stringify=False
)

format_reference_step = step(
    component=reference_formatter,
    input_map={"response": "response", "chunks": "chunks"},
    output_state="references",
)
