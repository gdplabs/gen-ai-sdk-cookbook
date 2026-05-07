## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gdplabs/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/tutorials/inference/catalog
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
   uv run catalog.py
   ```

4. **Expected Output**

   ```
   === Summarize Prompt ===
   [Message(role=<MessageRole.SYSTEM: 'system'>, contents=['You are an AI expert\nSummarize the following context.\n\nContext:\n```Some text to summarize```'], metadata={})]

   === Transform Query Prompt ===
   [Message(role=<MessageRole.USER: 'user'>, contents=['Transform the following query into a simpler form.\n\nQuery:\n```Complex query here```'], metadata={})]

   === Draft Document Prompt (default format) ===
   [Message(role=<MessageRole.SYSTEM: 'system'>, contents=['You are an AI expert.\nDraft a document following the provided format and context.\n\nFormat:\n```I. Background\nII. Content\nIII. Conclusion```'], metadata={}), Message(role=<MessageRole.USER: 'user'>, contents=['User instruction:\nWrite a summary report'], metadata={})]
   ```

## 📚 Reference

These examples are based on the [GL SDK GitBook documentation](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/inference/catalog).
