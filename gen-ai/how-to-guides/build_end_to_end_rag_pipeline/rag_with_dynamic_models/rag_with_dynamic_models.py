from gllm_generation.response_synthesizer import ResponseSynthesizer


def build_response_synthesizer(model_id: str) -> ResponseSynthesizer:
    """Build a response synthesizer for the given model.

    Args:
        model_id (str): The model identifier to use for the LM request processor.

    Returns:
        ResponseSynthesizer: Synthesizer configured with the given model.
    """
    return ResponseSynthesizer.preset.stuff(model_id)

