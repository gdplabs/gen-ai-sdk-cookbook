## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gdplabs/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/tutorials/core/tool
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
   uv run tool_quickstart.py
   ```

4. **Expected Output**

   ```
   Weather result: {'temperature': 22.5, 'conditions': 'sunny'}
   Weather via invoke: {'temperature': 22.5, 'conditions': 'sunny'}
   1 + 2 = 3
   Tool input schema: {'properties': {'a': {'description': 'First addend.', 'title': 'A', 'type': 'integer'}, 'b': {'description': 'Second addend.', 'title': 'B', 'type': 'integer'}}, 'required': ['a', 'b'], 'title': 'add_input', 'type': 'object'}
   ```

## 📚 Reference

These examples are based on the [GL SDK GitBook documentation](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/core/tool).
