## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/GDP-ADMIN/gen-ai-sdk-cookbook.git
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

3. **Run the examples**

   ```bash
   uv run custom_component.py
   uv run component_log_level_runtime_overhead.py
   ```

## 📚 Reference

These examples are based on the following GL SDK documentation:

- [Add a Custom Component (How-to Guide)](https://gdplabs.gitbook.io/sdk/how-to-guides/extend-lm-capabilities-with-custom-components)
- [Component Tutorial](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/core/component#adjust-log-level-for-lower-overhead-runs)
