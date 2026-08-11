# Chunk

Runnable examples for the `Chunk` schema in `gllm-core`.

A `Chunk` is the unit of retrieved content in GLLM Core: a primary `content` payload plus
the metadata, similarity score, and supplemental `additional_context` associated with it.
These examples focus on the `additional_context` field — a list of supplemental text or
binary items kept separate from the chunk's primary `content`, validated per item and
previewed in the chunk's string representation.

## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/GDP-ADMIN/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/tutorials/core/chunk/
   ```

2. **Set UV authentication and install dependencies**

   **For Unix-based systems (Linux, macOS):**

   ```bash
   ./setup.sh
   ```

   **For Windows:**

   ```cmd
   setup.bat
   ```

3. **Run the examples**

   ```bash
   uv run 001_chunk_basics.py        # Construct a Chunk with content + additional_context
   uv run 002_additional_context.py  # __repr__ preview and per-item validation
   ```

## 📚 Reference

These examples are based on the [GL SDK GitBook documentation](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/core/chunk).
