## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gdplabs/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/tutorials/data_store/build_data_store/
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
   ```

3. **Prepare `.env` file**

   Create a `.env` file (copy from `.env.example`) and fill in your values:
   ```env
   OPENAI_API_KEY="your-key-here"
   ```

5. **Run the example**

   ```bash
   uv run build_data_store.py
   ```
   ```bash
   uv run build_data_store_hybrid.py
   ```

> **Note**: build_data_store_hybrid.py requires Elasticsearch running on localhost:9200

## 📚 Reference

These examples are based on the [GL SDK GitBook documentation](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/data-store/build-data-store).
