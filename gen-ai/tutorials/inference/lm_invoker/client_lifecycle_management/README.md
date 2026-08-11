## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/GDP-ADMIN/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/tutorials/inference/lm_invoker/client_lifecycle_management/
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
   uv run ephemeral_client.py
   uv run persistent_client.py
   uv run client_manager_context_manager.py
   uv run client_manager_constructed.py
   uv run external_http_client.py
   uv run accessing_client.py
   ```

## 📚 Reference

These examples are based on the [GL SDK GitBook documentation](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/inference/lm-invoker/client-lifecycle-management).
