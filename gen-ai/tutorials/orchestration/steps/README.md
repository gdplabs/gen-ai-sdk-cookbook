## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gdplabs/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/tutorials/orchestration/steps
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

   | Script | Description | GitBook Section |
   |--------|-------------|-----------------|
   | `uv run basic_steps.py` | Basic steps: step, transform, bundle, copy, log, no_op, terminate | [Basic Steps](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/steps#basic-steps) |
   | `uv run branching_steps.py` | Branching steps: if_else, switch, toggle, guard | [Branching](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/steps#branching) |
   | `uv run concurrency_steps.py` | Concurrency steps: parallel, map_reduce (with Group, Val) | [Concurrency](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/steps#concurrency) |
   | `uv run flow_control_steps.py` | Flow control: while_do, try_catch, pause, goto, guard | [Flow Control](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/steps#flow-control) |
   | `uv run composition_steps.py` | Composition: log, subgraph | [Composition](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/steps#composition) |
   | `uv run pipeline_level_fallback.py` | Pipeline-level `fallback`/`catch` vs step-level `FallbackStepErrorHandler` | [Pipeline-Level Fallback](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/steps/error-handling#pipeline-level-fallback) |

## 📚 Reference

These examples are based on the [GL SDK GitBook documentation](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/steps).

### Notes

- **parallel**: In `gllm-pipeline` 0.5.18, `parallel()` with log-only branches (no `output_state`) can trigger `'NoneType' object is not iterable`. The cookbook uses branches with `output_state` for reliable execution.
- **subgraph**: The `output_state_map` parameter maps `{parent_state_key: subgraph_state_key}` — parent key first. The GitBook docs show the reversed order in some examples.