## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gdplabs/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/tutorials/retrieval/chunk_processor
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

   > Alternatively, set env vars manually:
   > ```env
   > UV_INDEX_GEN_AI_INTERNAL_USERNAME=oauth2accesstoken
   > UV_INDEX_GEN_AI_INTERNAL_PASSWORD="$(gcloud auth print-access-token)"
   > ```
   > Then run:
   > ```bash
   > uv lock
   > uv sync
   > ```

3. **Run the example**

   ```bash
   uv run chunk_processor.py
   ```

4. **Expected Output**

   ```
   [Chunk(id=chunk-1, content=Jakarta, Indonesia, metadata={'source': 'source-1'}, score=None), Chunk(id=chunk-2, content=Kuala Lumpur, Malaysia, metadata={'source': 'source-2', 'dupes': {'chunk-4': {'source': 'source-2'}}}, score=None), Chunk(id=chunk-3, content=Bangkok, Thailand, metadata={'source': 'source-3'}, score=None)]
   ```

## 📚 Reference

These examples are based on the [GL SDK GitBook documentation](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/retrieval/chunk-processor).
