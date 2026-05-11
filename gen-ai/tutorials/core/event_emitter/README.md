## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gdplabs/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/tutorials/core/event_emitter
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
   uv run event_emitter.py
   ```

4. **Expected Output**

   ```
   {"id":null,"value":"Hello, world!","value_type":"text","level":"INFO","type":"response","timestamp":"...","metadata":{}}
   {"id":null,"value":"This is a warning!","value_type":"text","level":"WARN","type":"response","timestamp":"...","metadata":{}}
   ```

   Note: The debug message is filtered out since the emitter is configured with minimum level INFO.

## 📚 Reference

These examples are based on the [GL SDK GitBook documentation](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/core/event-emitter).
