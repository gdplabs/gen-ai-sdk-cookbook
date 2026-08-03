## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gdplabs/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/tutorials/core/logger_manager/
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
   uv run logger_manager.py         # Quickstart: basic logger usage
   uv run getting_loggers.py        # Getting root and child loggers
   uv run configuring_levels.py     # Setting log levels and formats
   uv run adding_handlers.py        # Adding custom file handlers
   uv run json_error_payloads.py    # JSON error payload logging
   uv run global_json_fields.py     # Attaching global fields to every JSON log record
   ```

## 📚 Reference

These examples are based on the [GL SDK GitBook documentation tutorial page](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/core/logger-manager).