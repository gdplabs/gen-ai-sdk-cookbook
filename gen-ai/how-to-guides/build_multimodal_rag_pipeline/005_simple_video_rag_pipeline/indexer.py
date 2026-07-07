VIDEOS = [
    {
        "url": "https://youtu.be/f_uwKZIAeM0?si=zHbqxKAEvVhht5GZ",
        "title": "What is Machine Learning?",
    },
]


async def index_videos() -> None:
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
