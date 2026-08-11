# Orchestration Routing Tutorial

Code examples for [GL SDK Routing tutorial](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/routing).

## Router examples

Each router is a standalone directory with its own `setup.sh` / `setup.bat`:

| Directory | Description |
|-----------|-------------|
| [rule-based-router/](rule-based-router/) | Deterministic keyword matching |
| [semantic-router/](semantic-router/) | Native semantic similarity backend |
| [lm-based-router/](lm-based-router/) | LM Router (LM-based routing) |
| [classifier-router/](classifier-router/) | Pre-trained MLP/SVM classifier routing |
| [similarity-based-router/](similarity-based-router/) | Deprecated v0.5 similarity router |

## Setup

```bash
cd <router-directory>
bash setup.sh
uv run python <script>.py
```

Note: Router examples require network access and an `OPENAI_API_KEY`.

> **Note (lm-based-router):** `lm_router.py` now uses the `LMRouter` API
> (`gllm_pipeline.router.LMRouter`, constructed directly with an
> `lm_invoker`). `LMRouter` ships in `gllm-pipeline` **v0.6.0**, which has not
> been published to PyPI yet (latest published is 0.5.20 as of this sync).
> The `pyproject.toml` is pinned to `gllm-pipeline[llmrouter]>=0.6.0,<0.7.0`
> so it resolves once v0.6.0 is released. Until then `uv run` is blocked on the
> v0.6.0 release (runtime verification pending); the code matches the
> [GL SDK routing docs](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/routing/lm-based-router).
> This mirrors [gl-sdk#5707](https://github.com/GDP-ADMIN/gl-sdk/pull/5707)
> and [gl-sdk#5979](https://github.com/GDP-ADMIN/gl-sdk/pull/5979).

Reference:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/routing
