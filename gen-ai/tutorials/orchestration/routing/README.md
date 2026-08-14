# Orchestration Routing Tutorial

Code examples for [GL SDK Routing tutorial](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/routing).

## Router examples

Each router is a standalone directory with its own `setup.sh` / `setup.bat`:

| Directory | Description |
|-----------|-------------|
| [rule-based-router/](rule-based-router/) | Deterministic keyword matching |
| [semantic-router/](semantic-router/) | Native semantic similarity backend |
| [lm-router/](lm-router/) | LM Router (LM-based routing) |
| [classifier-router/](classifier-router/) | Pre-trained MLP/SVM classifier routing |
| [similarity-based-router/](similarity-based-router/) | Deprecated v0.5 similarity router |

## Setup

```bash
cd <router-directory>
bash setup.sh
uv run python <script>.py
```

Note: Router examples require network access and an `OPENAI_API_KEY`.

Reference:
    https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/routing
