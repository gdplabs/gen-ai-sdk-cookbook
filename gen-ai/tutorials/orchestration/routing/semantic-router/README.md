# Semantic Router

Cookbook coverage for [`/sdk/gen-ai-sdk/tutorials/orchestration/routing/semantic-router`](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/routing/semantic-router).

## Run

```bash
cd "$(dirname "$0")"
bash setup.sh
```

Most examples need an embedding-model credential.

## Examples

| Script | GitBook section | Run |
| --- | --- | --- |
| `semantic_router_native.py` | Native backend | `uv run python semantic_router_native.py` |
| `semantic_router_aurelio.py` | Aurelio backend with EM Invoker | `uv run python semantic_router_aurelio.py` |
| `semantic_router_aurelio_encoder.py` | Aurelio backend with `EMInvokerEncoder` | `uv run python semantic_router_aurelio_encoder.py` |
| `semantic_router_knn.py` | KNN backend | `uv run python semantic_router_knn.py` |
| `semantic_router_preset.py` | Presets | `uv run python semantic_router_preset.py` |

## Notes

- Router subpackage imports can pull `torch` transitively at import time.
- If a script is blocked by an unavailable backend dependency, keep it here and add the exact blocker to this README instead of deleting it.
- KNN requires `gllm-pipeline[llmrouter]`. Aurelio examples use paths exposed in the entry `pyproject.toml`.
