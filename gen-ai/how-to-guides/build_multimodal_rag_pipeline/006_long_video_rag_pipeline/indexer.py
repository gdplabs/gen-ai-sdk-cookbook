"""Example script to index a YouTube video by transcript segments into a vector store.

References:
    [1] https://gdplabs.gitbook.io/sdk/gen-ai-sdk/guides/build-multimodal-rag-pipeline/video-search-pipeline
"""

import asyncio
import hashlib
import os
import tempfile
import traceback

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
        "url": "https://youtu.be/QRjCh-lcKW4?si=a_xNMblRujAw55zL",
        "title": "Attention Is All You Need",
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
        video_id = hashlib.md5(video["url"].encode()).hexdigest()

        with tempfile.TemporaryDirectory() as tmpdir:
            out_path = os.path.join(tmpdir, "video.mp4")
            proc = await asyncio.create_subprocess_exec(
                "yt-dlp", "-vU -o", out_path, "--merge-output-format", "mp4", video["url"],
            )
            await proc.wait()
            if proc.returncode != 0:
                raise RuntimeError(f"yt-dlp failed for {video['url']}")
            result = await video_converter.convert(
                out_path,
                text_one_liner=video["title"],
            )

        # Index the overall video summary as a standalone chunk
        chunks.append(
            Chunk(
                content=result.result,
                metadata={
                    "video_id": video_id,
                    "url": video["url"],
                    "title": video["title"],
                    "chunk_type": "summary",
                    "start_time": 0.0,
                    "end_time": 0.0,
                },
            )
        )

        # Index each segment separately so the pipeline can cite exact timestamps
        for seg_dict in result.metadata.get("segments", []):
            segment = Segment(**seg_dict)
            segment_text = " ".join(segment.segment_caption)
            if not segment_text:
                continue

            start = segment.start_time or 0.0
            end = segment.end_time or 0.0
            chunks.append(
                Chunk(
                    content=segment_text,
                    metadata={
                        "video_id": video_id,
                        "url": video["url"],
                        "title": video["title"],
                        "chunk_type": "segment",
                        "start_time": start,
                        "end_time": end,
                        "timestamp": format_timestamp(start),
                        "keyframe_count": len(segment.keyframes),
                        "transcript_count": len(segment.transcripts),
                    },
                )
            )

        print(
            f"Processed '{video['title']}': "
            f"{len(result.metadata.get('segments', []))} segments\n"
            f"  Summary: {result.result}...\n"
            f"  1st segment: {result.metadata.get('segments', [])[0]}...\n"
        )



    await data_store.vector.create(chunks)
    print(f"Indexed {len(chunks)} chunks.")


if __name__ == "__main__":
    asyncio.run(index_videos())
