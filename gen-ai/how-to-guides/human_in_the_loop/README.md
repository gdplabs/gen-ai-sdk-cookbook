## ⚙️ Prerequisites

Please refer to prerequisites [here](../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gdplabs/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/how-to-guides/human_in_the_loop
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
   uv run hitl_orchestration.py
   uv run datastore_saver.py
   ```

4. **Expected Output**

   ```text
   Expected output will be added after verification.
   ```

## 📚 Reference

These examples are based on the [GL SDK GitBook documentation](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/guides/human-in-the-loop).

| Script | Description |
|---|---|
| `uv run hitl_orchestration.py` | Basic HITL flow with an in-memory `MemorySaver` checkpointer. |
| `uv run datastore_saver.py` | Durable HITL flow backed by `DataStoreSaver`, so paused threads survive a process restart. See [Running with Session Persistence](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/guides/human-in-the-loop#2-running-with-session-persistence). |
