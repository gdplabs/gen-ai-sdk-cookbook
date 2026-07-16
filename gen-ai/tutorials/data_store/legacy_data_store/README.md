## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gdplabs/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/tutorials/data_store/legacy_data_store/
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

3. **Prepare `.env` file**

   Create a `.env` file (copy from `.env.example`) and fill in your values:
   ```env
   OPENAI_API_KEY="your-key-here"
   ```

4. **Run the examples**

   ```bash
   uv run quickstart.py
   uv run metadata_filtering.py
   uv run cache.py
   ```

> **Note**: These examples use the legacy `ChromaVectorDataStore` API which
> will be deprecated in `gllm-datastore` v0.6.0. For new projects, use the
> [Data Store](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/data-store) API instead.

## 📚 Reference

These examples are based on the [GL SDK GitBook documentation — Vector Data Store (Legacy)](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/data-store/legacy/vector-data-store).
