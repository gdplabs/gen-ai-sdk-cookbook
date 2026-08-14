## Prerequisites

Please refer to prerequisites [here](../../README.md).

## Getting Started

[uv](https://docs.astral.sh/uv/) manages the project environment. Install
dependencies using [`setup.sh`](./setup.sh) (Linux/macOS) or
[`setup.bat`](./setup.bat) (Windows).

## Usage

| Script | Description |
|--------|-------------|
| `uv run debug_tracing.py` | Enable per-node debug tracing |
| `uv run step_outputs.py` | Capture intermediate step outputs |
| `uv run state_history.py` | Iterate checkpointed state history |
| `uv run fork_pipeline.py` | Fork execution from a checkpoint |
| `uv run datastore_saver.py` | Persist checkpoints to a `DataStoreSaver`-backed datastore instead of memory |

## Reference

These examples are based on the [GL SDK GitBook documentation for Observability and Debugging](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/observability-and-debugging).