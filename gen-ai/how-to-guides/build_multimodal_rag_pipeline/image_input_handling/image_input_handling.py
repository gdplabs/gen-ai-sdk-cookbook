from typing import Any

from gllm_pipeline.pipeline.states import RAGState
from gllm_multimodal.modality_converter.image_to_text.image_to_caption import LMBasedImageToCaption
from gllm_pipeline.steps import step, transform

...

class ImageSearchByImageState(RAGState):
    image_path: str
