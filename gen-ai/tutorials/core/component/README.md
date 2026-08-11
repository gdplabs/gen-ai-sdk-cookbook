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
   uv run 001_quickstart.py            # Tutorial: define and execute with @main
   uv run 002_abstract_component.py    # Tutorial: @main with abstract classes
   uv run 003_override_main.py         # Tutorial: overriding @main in subclasses
   uv run 004_component_log_level_runtime_overhead.py # Tutorial: component lifecycle and runtime behavior
   uv run 005_global_log_level.py                 # Tutorial: set a global log level for all components
   uv run 006_legacy_component.py      # Tutorial: backwards-compatible _run components
   ```

## 🌐 Set a Global Log Level for All Components

Setting `log_level` on each instance is convenient for a handful of components, but suppressing IO-event logging **app-wide** — to quiet every component in a large pipeline, or to flip the level at startup — is tedious and easy to miss when done per-instance.

`Component.set_global_log_level(level)` is a classmethod that sets a single default applied to **all existing and future** `Component` instances. One call replaces the need to touch every instance.

**Per-instance overrides still win.** After a global call, you can still raise or lower a single component by assigning its `log_level` directly — that explicit override takes precedence for that component.

**A new global call resets prior overrides.** Calling `set_global_log_level` again clears each component's accumulated per-instance setting and re-applies the new global level. If you want a specific component to diverge *after* a later global change, assign its `log_level` again.

Precedence (later rules win):

1. **Default `DEBUG`** — used until anything else is set.
2. **Global `Component.set_global_log_level(...)`** — becomes the default for all existing and future components.
3. **Per-instance `component.log_level = ...`** — takes precedence for that component, even after a global change.
4. **A *new* `set_global_log_level(...)` call** — resets all per-instance overrides back to the new global level.

Invalid levels are rejected with `ValueError`.

## 📚 References

These examples are based on the following GL SDK documentation:

- [How-to-Guide: Add a Custom Component](https://gdplabs.gitbook.io/sdk/how-to-guides/add-a-custom-component)
- [Tutorial: Component](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/core/component)
