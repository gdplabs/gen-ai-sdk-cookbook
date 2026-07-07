import asyncio
from gllm_core.schema import Chunk
from gllm_core.constants import DefaultChunkMetadata
from gllm_retrieval.chunk_processor import MergingChunkProcessor

prev_id_key = DefaultChunkMetadata.PREV_CHUNK_ID
next_id_key = DefaultChunkMetadata.NEXT_CHUNK_ID

chunks = [
    Chunk(
        id="chunk1",
        content="Hello World!",
        metadata={prev_id_key: "chunk0", next_id_key: "chunk2"},
    ),
    Chunk(
        id="chunk3",
        content="beautiful today, isn't it?",
        metadata={prev_id_key: "chunk2", next_id_key: "chunk4"},
    ),
    Chunk(
        id="chunk2",
        content="World! It is beautiful",
        metadata={prev_id_key: "chunk1", next_id_key: "chunk3"},
    ),
]

processor = MergingChunkProcessor()
result = asyncio.run(processor.process_chunks(chunks))
print(result)
# Chunks 1-2-3 form a contiguous chain and are merged into one chunk:
# [Chunk(id='chunk1-chunk2-chunk3', content='Hello World!\nIt is beautiful today, isn\'t it?', ...)]
