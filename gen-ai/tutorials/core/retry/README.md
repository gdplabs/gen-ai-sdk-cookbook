## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gdplabs/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/tutorials/core/retry/
   ```

2. **Set UV authentication and install dependencies**  
   Run the appropriate setup script for your system:

   **For Unix-based systems (Linux, macOS):**
   ```bash
   ./setup.sh
   ```

   **For Windows:**
   ```cmd
   setup.bat
   ```

   > Alternatively, set the following env vars manually
   > ```env
   > UV_INDEX_GEN_AI_INTERNAL_USERNAME=oauth2accesstoken
   > UV_INDEX_GEN_AI_INTERNAL_PASSWORD="$(gcloud auth print-access-token)"
   > ```
   > 
   > *Then run*
   > ```bash
   > uv lock
   > uv sync
   > ```

3. **Run the examples**

   ```bash
   uv run retry_quickstart.py     # Quickstart: decorator + direct execution
   uv run retry_config.py        # RetryConfig: controlling retry behavior
   uv run decorator_usage.py     # Decorator on async, sync, and class methods
   uv run backoff_and_jitter.py   # Exponential backoff and jitter configuration
   uv run timeout_usage.py       # Overall timeout for retry operations
   uv run exception_handling.py  # Controlling which exceptions trigger retries
   ```

## 📚 Reference

These examples are based on the [GL SDK Gitbook documentation tutorial page](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/core/retry).