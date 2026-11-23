## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gdplabs/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/tutorials/core/dynamic_component/
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
   uv run dynamic_component.py   # Quickstart: DynamicComponent with Lazy bindings
   uv run to_dynamic.py          # Using Component.to_dynamic() class method
   uv run instance_caching.py    # Instance caching with cache_instances=True
   ```

## 📚 Reference

These examples are based on the [GL SDK GitBook documentation tutorial page](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/core/dynamic-component).