## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gdplabs/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/tutorials/orchestration/pipelines-and-agents
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
   | `uv run pipeline_as_tool.py` | Convert a Pipeline into a callable Tool for Agent integration | [Pipeline-as-a-Tool](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/pipelines-and-agents#pipeline-as-a-tool) |
   | `uv run agent_as_step.py` | Wrap an Agent as a Pipeline Step for deterministic flow with reasoning | [Agent-as-a-Step](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/pipelines-and-agents#agent-as-a-step) |

## 📚 Reference

These examples are based on the [GL SDK GitBook documentation](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/pipelines-and-agents).

### Notes

- **gllm-aip not required**: These scripts demonstrate the integration patterns without requiring `gllm-aip` (the Agent package). `pipeline_as_tool.py` uses the `Pipeline.as_tool()` API directly. `agent_as_step.py` uses a `MockAgent` class that mimics the `Agent.run()` interface — replace it with a real `gllm_aip.Agent` in production.
- **Pipeline-as-a-Tool**: Every `Component` and `Pipeline` in the SDK has an `.as_tool()` method that produces a `Tool` with input/output schemas. An Agent uses these schemas to decide when to invoke the pipeline.
- **Agent-as-a-Step**: Wrap an Agent in a custom `Component` (with `@main` decorator) to embed it as a step. The pipeline controls execution order while the agent handles reasoning at specific stages.