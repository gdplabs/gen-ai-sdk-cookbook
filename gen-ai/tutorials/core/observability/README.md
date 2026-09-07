## ⚙️ Prerequisites

Please refer to prerequisites [here](../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gdplabs/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/tutorials/core/observability
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
   uv run 001_component_spans.py   # Component.run() emits a span named after the class
   uv run 002_capturing_io.py      # configure_component_io_capture -> gllm.component.input/output on the span
   uv run 003_scoping_capture.py   # capture_content(...) -> capture applies inside the block only
   ```

4. **Expected Output**

   `001_component_spans.py` — every `Component.run()` emits a span named after the class:

   ```text
   Greeter {'gllm.component.name': 'Greeter'}
   ```

   `002_capturing_io.py` — with `configure_component_io_capture` enabled, the span also carries the input and output:

   ```text
   Greeter {'gllm.component.name': 'Greeter', 'gllm.component.input': '{"name":"world"}', 'gllm.component.output': '"Hello, world!"'}
   ```

   `003_scoping_capture.py` — `capture_content` scopes the override to the block; outside it the process-wide default applies:

   ```text
   outside scope, input captured: False
   inside scope, input captured: True
   Greeter {'gllm.component.name': 'Greeter', 'gllm.component.input': '{"name":"inside-scope"}', 'gllm.component.output': '"Hello, inside-scope!"'}
   ```

## 📚 Reference

These examples are based on the [GL SDK GitBook documentation](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/core/observability).
