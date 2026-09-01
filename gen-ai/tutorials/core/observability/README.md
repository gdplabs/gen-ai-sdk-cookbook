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
   uv run component_spans.py
   uv run capturing_io.py
   uv run shared_tracer.py
   ```

4. **Expected Output**

   `component_spans.py` — every `Component.run()` emits a span named after the class:

   ```text
   Greeter {'gllm.component.name': 'Greeter'}
   ```

   `capturing_io.py` — with `configure_component_io_capture` enabled, the span also carries the input and output:

   ```text
   Greeter {'gllm.component.name': 'Greeter', 'gllm.component.input': '{"name":"world"}', 'gllm.component.output': '"Hello, world!"'}
   ```

   `shared_tracer.py` — using `get_tracer()` and `SpanAttribute` directly:

   ```text
   my-span {'gllm.component.name': 'MyComponent'}
   ```

## 📚 Reference

These examples are based on the [GL SDK GitBook documentation](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/core/observability).
