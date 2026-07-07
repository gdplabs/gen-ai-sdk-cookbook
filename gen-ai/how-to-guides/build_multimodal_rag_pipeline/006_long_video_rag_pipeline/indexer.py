import hashlib

VIDEOS = [
    {
        "url": "https://youtu.be/QRjCh-lcKW4?si=a_xNMblRujAw55zL",
        "title": "Attention Is All You Need",
    },
]


def format_timestamp(seconds: float) -> str:
    m, s = divmod(int(seconds), 60)
    return f"{m:02d}:{s:02d}"


async def index_videos() -> None:
    chunks = []

    for video in VIDEOS:
        video_id = hashlib.md5(video["url"].encode()).hexdigest()

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

        # Index the overall video summary as the parent chunk
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

        # Index each segment as a child chunk linked back to the parent via video_id
        for seg_dict in result.metadata.get("segments", []):
            segment = Segment(**seg_dict)
            segment_text = " ".join(segment.segment_caption) or " ".join(t.text for t in segment.transcripts)
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
            f"  Summary: {result.result[:120}...\n"
        )

    await data_store.vector.create(chunks)
    print(f"Indexed {len(chunks)} chunks.")


if __name__ == "__main__":
    asyncio.run(index_videos())
