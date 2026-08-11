## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../../README.md).

## 🧭 Schema Inference (what's new)

gllm-pipeline can now **infer** key-only state/input schemas directly from the
steps you pass in — without executing your code — when you omit `state_type`
and/or `input_type`. The constructor gains an `infer_schema` switch:

- `None` (default, **best-effort**): attempt inference; silently fall back to the
  prior behavior (`RAGState` for state, no input schema) when inference is unsafe.
- `True` (**strict**): raise `PipelineSchemaError` if inference is unsafe for any step.
- `False` (**disabled**): never infer; keep the old default behavior exactly.

Inferred schemas are key-only (`Any` values) and are not a substitute for a real
validation contract — use an explicit `state_type`/`input_type` when you need
precise types or runtime validation. See the two scripts below for runnable demos.

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gdplabs/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/tutorials/orchestration/pipeline
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

   > Alternatively, set env vars manually:
   > ```env
   > UV_INDEX_GEN_AI_INTERNAL_USERNAME=oauth2accesstoken
   > UV_INDEX_GEN_AI_INTERNAL_PASSWORD="$(gcloud auth print-access-token)"
   > ```
   > Then run:
   > ```bash
   > uv lock
   > uv sync
   > ```

3. **Run the examples**

   | Script | Description | GitBook Section |
   |--------|-------------|----------------|
   | `uv run pipeline.py` | Quickstart: create and invoke a simple Pipeline | [Quickstart](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/pipeline#quickstart) |
   | `uv run pipe_operator.py` | Compose a Pipeline using the pipe `|` operator | [The Pipe Operator](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/pipeline#the-pipe-operator) |
   | `uv run append_step.py` | Append a step to an existing Pipeline | [Appending a Step](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/pipeline#appending-a-step) |
   | `uv run merge_pipelines.py` | Merge two Pipelines of the same State schema | [Merge Two Pipelines](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/pipeline#merge-two-pipelines) |
   | `uv run placeholder_pipeline.py` | Use a placeholder (empty) Pipeline with `|` | [Placeholder Pipelines](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/pipeline#placeholder-pipelines) |
   | `uv run visualize_pipeline.py` | Visualize a Pipeline using `get_mermaid_diagram()` | [Visualizing the Pipeline](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/pipeline#visualizing-the-pipeline) |
   | `uv run runtime_config.py` | Runtime Configuration with config-driven switches | [Runtime Configuration](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/pipeline#runtime-configuration) |
   | `uv run runtime_config_component.py` | Runtime Configuration with Component condition and `if_else` | [Runtime Configuration](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/pipeline#runtime-configuration) |
   | `uv run input_output_schema_typeddict.py` | Input/Output schema filtering with TypedDict | [Using TypedDict for Simple Schemas](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/pipeline#using-typeddict-for-simple-schemas) |
   | `uv run input_output_schema_pydantic.py` | Input/Output schema with Pydantic validation | [Using Pydantic for Validation](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/pipeline#using-pydantic-for-validation) |
   | `uv run pipeline_as_tool.py` | Convert a Pipeline to a Tool for Agent integration | [Converting to a Tool](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/pipeline#converting-to-a-tool) |
   | `uv run debug_state.py` | Use the Debug State trace to inspect execution | [Using the Debug State](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/pipeline#using-the-debug-state) |
   | `uv run subgraph_pipeline.py` | Use a Pipeline as a Subgraph via `subgraph()` | [Using a Pipeline as a Subgraph](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/pipeline#using-a-pipeline-as-a-subgraph) |
   | `uv run subgraph_leftshift.py` | Embed a Pipeline as a subgraph via the `<<` operator | [Using the Leftshift (<<) Operator](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/pipeline#using-the-leftshift-operator) |
   | `uv run schema_inference_best_effort.py` | Best-effort schema inference when `state_type`/`input_type` are omitted | [Auto-inferring State and Input Schemas](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/pipeline#example-best-effort-inference) |
   | `uv run schema_inference_strict.py` | Strict inference (`infer_schema=True`) raising `PipelineSchemaError` on unsafe steps | [Auto-inferring State and Input Schemas](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/pipeline#example-strict-inference-with-an-unsafe-step) |

## 📚 Reference

These examples are based on the [GL SDK GitBook documentation](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/pipeline).
