"""Example script to index a YouTube video by transcript segments into a vector store.

Authors:
    Nico Samuelson Tjandra (nico.s.tjandra@gdplabs.id)

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/guides/build-multimodal-rag-pipeline/video-search-pipeline
"""

import asyncio
import json
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

VIDEOS = [
    {
        "url": "https://youtu.be/f_uwKZIAeM0?si=zHbqxKAEvVhht5GZ",
        "title": "What is Machine Learning?",
    },
]

# Initialize vector store
em_invoker = VoyageEMInvoker(model_name=os.getenv("EMBEDDING_MODEL"))
data_store = ChromaDataStore(
    collection_name="video-qa",
    client_type=ChromaClientType.PERSISTENT,
    persist_directory="data",
).with_vector(em_invoker=em_invoker)

video_converter = HybridVideoToCaption.from_preset("e2e_audio_driven")
video_converter.denormalize_time = False

def format_timestamp(seconds: float) -> str:
    """Convert a duration in seconds to a MM:SS timestamp string.

    Args:
        seconds (float): Duration in seconds.

    Returns:
        str: Zero-padded MM:SS timestamp (e.g. ``"03:45"``).
    """
    m, s = divmod(int(seconds), 60)
    return f"{m:02d}:{s:02d}"


async def index_videos() -> None:
    """Download, transcribe, and index the configured YouTube videos into the vector store.

    For each video, downloads the mp4 via yt-dlp, runs HybridVideoToCaption to generate
    a summary and segment-level captions, then indexes the overall summary and each
    segment as separate chunks (with timestamp metadata) into ChromaDB. Prints progress
    and a final count of indexed chunks.

    Raises:
        RuntimeError: If yt-dlp exits with a non-zero return code for any video.
    """
    chunks = []

    for video in VIDEOS:
        with tempfile.TemporaryDirectory() as tmpdir:
            out_path = os.path.join(tmpdir, "video.mp4")
            proc = await asyncio.create_subprocess_exec(
                "yt-dlp", "-o", out_path, "--merge-output-format", "mp4", video["url"],
            )
            await proc.wait()
            if proc.returncode != 0:
                raise RuntimeError(f"yt-dlp failed for {video['url']}")
            result = await video_converter.convert(
                out_path,
                text_one_liner=video["title"],
            )

        # Build content and store segment timestamps/transcripts as JSON metadata
        segment_texts = []
        segments = []
        for seg_dict in result.metadata.get("segments", []):
            segment = Segment(**seg_dict)
            text = " ".join(segment.segment_caption) or " ".join(t.text for t in segment.transcripts)
            if not text:
                continue
            segment_texts.append(text)
            segments.append(
                {
                    "start_time": segment.start_time or 0.0,
                    "end_time": segment.end_time or 0.0,
                    "transcript": " ".join(t.text for t in segment.transcripts),
                }
            )

        # Combine summary and all segment captions into one chunk
        content = result.result
        if segment_texts:
            content += "\n\n" + "\n".join(segment_texts)

        chunks.append(
            Chunk(
                content=content,
                metadata={
                    "url": video["url"],
                    "title": video["title"],
                    "segment_count": len(segment_texts),
                    "segments": json.dumps(segments),
                },
            )
        )

        print(
            f"Processed '{video['title']}': {len(segment_texts)} segments\n"
            f"  Summary: {result.result}...\n"
        )

    await data_store.vector.create(chunks)
    print(f"Indexed {len(chunks)} chunks.")


if __name__ == "__main__":
    asyncio.run(index_videos())
