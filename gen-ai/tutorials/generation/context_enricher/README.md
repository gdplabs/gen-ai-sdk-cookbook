## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gdplabs/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/tutorials/generation/context_enricher
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
   uv run context_enricher.py
   ```

4. **Expected Output**

   ```
   - title: Intro to DL
   - source: docs://ml101
   - page: 3
   - tags: ml, basics
   ---
   Neural networks learn by gradient descent.
   ```

## 📚 Reference

These examples are based on the [GL SDK GitBook documentation](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/generation/context-enricher).
