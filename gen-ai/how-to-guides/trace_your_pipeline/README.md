## ⚙️ Prerequisites

Please refer to prerequisites [here](../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gdplabs/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/how-to-guides/trace_your_pipeline
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

3. **Run the example**

   ```bash
   uv run trace_pipeline.py
   ```

4. **Expected Output**

   ```text
   [short] HI | score=2
   [LONG] HELLO, WORLD! | score=13
   Captured 12 spans
   pipeline.step.uppercase
   pipeline.step.score
   Labeler
     gllm.component.name: Labeler
     gllm.component.input: {"uppercase_text":"HI","score":2}
     gllm.component.output: "[short] HI"
   pipeline.step.label_text
   pipeline.step.finalize
   pipeline.invoke.my_pipeline_service
   pipeline.step.uppercase
   pipeline.step.score
   Labeler
     gllm.component.name: Labeler
     gllm.component.input: {"uppercase_text":"HELLO, WORLD!","score":13}
     gllm.component.output: "[LONG] HELLO, WORLD!"
   pipeline.step.label_text
   pipeline.step.finalize
   pipeline.invoke.my_pipeline_service
   ```

   The `Labeler` component span carries `gllm.component.input` / `gllm.component.output`
   because `configure_component_io_capture(...)` is enabled at the top of the script.
   Plain `BasePipelineStep` steps emit only `pipeline.step.*` spans.

## 📚 Reference

These examples are based on the [GL SDK GitBook documentation](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/guides/trace-your-pipeline).
