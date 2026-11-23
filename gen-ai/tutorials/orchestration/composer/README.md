## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gdplabs/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/tutorials/orchestration/composer
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
   | `uv run basic_composer.py` | Basic Composer methods: step, transform, bundle, log, no_op, terminate | [Basic Composer Methods](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/composer#basic-composer-methods) |
   | `uv run branching_composer.py` | Direct-style branching: if_else, switch, toggle, guard | [Branching](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/composer#branching) |
   | `uv run builder_style_composer.py` | Builder-style branching: when/then/otherwise, switch/case/default, toggle/then, guard/on_success, parallel/fork | [Branching](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/composer#branching) |
   | `uv run concurrency_composer.py` | Concurrency: parallel, map_reduce (with Group) | [Concurrency](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/composer#concurrency) |
   | `uv run composition_composer.py` | Composition: subgraph | [Composition](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/composer#composition) |

## 📚 Reference

These examples are based on the [GL SDK GitBook documentation](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/composer).

### Notes

- **Builder-style branches**: In `gllm-pipeline` 0.5.18, builder-style branching (`.when().then()`, `.switch().case()`, etc.) must use step objects — not `Pipeline` objects — as branch arguments. Passing a `Pipeline` as a branch triggers `AttributeError: 'Pipeline' object has no attribute 'is_excluded'` during graph compilation. The GitBook examples use `Pipeline` objects; this cookbook uses steps until the library fix lands.
- **parallel**: Branches that produce state output (via `output_state`) merge correctly. Log-only branches (no `output_state`) can trigger `'NoneType' object is not iterable` in 0.5.18.
- **subgraph**: The `output_state_map` parameter maps `{parent_state_key: subgraph_state_key}` — parent key first. The GitBook docs show the reversed order in some examples.