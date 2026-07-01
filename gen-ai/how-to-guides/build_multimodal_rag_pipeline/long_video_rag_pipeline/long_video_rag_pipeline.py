import asyncio
import os
import tempfile

from dotenv import load_dotenv
from gllm_core.schema import Chunk
from gllm_datastore.data_store import ChromaDataStore
from gllm_datastore.data_store.chroma.data_store import ChromaClientType
from gllm_inference.em_invoker import VoyageEMInvoker
from gllm_multimodal.modality_converter.video_to_text.video_to_caption.hybrid_video_to_caption import (
    HybridVideoToCaption,
)
from gllm_multimodal.schema.video_caption_result import Segment

load_dotenv()

em_invoker = VoyageEMInvoker(os.getenv("EMBEDDING_MODEL"))
data_store = ChromaDataStore(
    collection_name="video-qa",
    client_type=ChromaClientType.PERSISTENT,
    persist_directory="data",
).with_vector(em_invoker=em_invoker)

video_converter = HybridVideoToCaption.from_preset("e2e_audio_driven")
