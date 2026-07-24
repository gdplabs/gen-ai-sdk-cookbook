## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gdplabs/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/tutorials/core/component/
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
   uv run custom_component.py      # How-to-guide: custom component with _run
   uv run quickstart.py            # Tutorial: define and execute with @main
   uv run abstract_component.py    # Tutorial: @main with abstract classes
   uv run override_main.py         # Tutorial: overriding @main in subclasses
   uv run legacy_component.py      # Tutorial: backwards-compatible _run components
   uv run component_log_level_runtime_overhead.py #Tutorial: component lifecycle and runtime behavior
   ```

## 📚 References

These examples are based on the following GL SDK documentation:

- [How-to-Guide: Add a Custom Component](https://gdplabs.gitbook.io/sdk/how-to-guides/add-a-custom-component)
- [Tutorial: Component](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/core/component)
