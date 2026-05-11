## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gdplabs/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/tutorials/inference/prompt_builder
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
   uv run prompt_builder.py
   ```

4. **Expected Output**

   ```
   === Quickstart ===
   [Message(role=<MessageRole.SYSTEM: 'system'>, contents=['Talk like a pirate.'], metadata={}), Message(role=<MessageRole.USER: 'user'>, contents=['What is the capital city of Indonesia?'], metadata={})]

   === Prompt Variables ===
   [Message(role=<MessageRole.SYSTEM: 'system'>, contents=['Talk like a pirate.'], metadata={}), Message(role=<MessageRole.USER: 'user'>, contents=['What is the capital city of Indonesia?'], metadata={})]

   === With History ===
   [Message(role=<MessageRole.SYSTEM: 'system'>, contents=['Talk like a pirate.'], metadata={}), Message(role=<MessageRole.USER: 'user'>, contents=['Hi, there!'], metadata={}), Message(role=<MessageRole.ASSISTANT: 'assistant'>, contents=['Hello!'], metadata={}), Message(role=<MessageRole.USER: 'user'>, contents=['What is the capital city of Indonesia?'], metadata={})]
   ```

## 📚 Reference

These examples are based on the [GL SDK GitBook documentation](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/inference/prompt-builder).
