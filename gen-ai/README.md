# 🍳 Gen AI SDK Cookbook

Welcome to the **Gen AI SDK Cookbook** — your collection of runnable examples for the [GL Generative AI SDK](https://docs.gdplabs.id/gen-ai-sdk).

The SDK documentation explains concepts and APIs. This cookbook shows working code.

## ⚙️ Prerequisites

1. **OpenAI API key** — See <https://platform.openai.com/api-keys>
2. **UV** — See <https://docs.astral.sh/uv/>
3. **Python 3.11+** — Can be [installed via UV](https://docs.astral.sh/uv/guides/install-python/)
4. **gcloud CLI** — See <https://cloud.google.com/sdk/docs/install>, then run `gcloud auth login`

## 🚀 Where to Start

| I want to... | Go to |
|---|---|
| Build a RAG pipeline step by step | [`guides/build_end_to_end_rag_pipeline/`](./guides/build_end_to_end_rag_pipeline/) |
| Integrate with a UI (Next.js / Vite) | [`guides/a2ui/`](./guides/a2ui/) |
| Learn how to call a language model | [`tutorials/inference/lm_invoker/`](./tutorials/inference/lm_invoker/) |
| Add streaming, structured output, or tool calling | [`tutorials/inference/lm_request_processor/`](./tutorials/inference/lm_request_processor/) |
| Connect a vector or SQL data store | [`tutorials/data_store/`](./tutorials/data_store/) |
| Evaluate my pipeline | [`tutorials/evaluation/`](./tutorials/evaluation/) |
| Add deep research capability | [`examples/deep_researcher/`](./examples/deep_researcher/) |
| Add realtime voice interaction | [`tutorials/inference/realtime_session/`](./tutorials/inference/realtime_session/) |
| Build a custom pipeline component | [`tutorials/core/custom_component/`](./tutorials/core/custom_component/) |

## 📁 Structure

```
gen-ai/
├── guides/       # goal-oriented walkthroughs → guides/README.md
├── tutorials/    # component deep dives       → tutorials/README.md
└── examples/     # uncategorized / WIP
    └── deep_researcher/
```

Every example folder follows the same convention:

```
<example>/
├── README.md        # what it does, how to run it, link to docs
├── .env.example     # required environment variables
├── .python-version
├── pyproject.toml
├── setup.sh
├── setup.bat
└── *.py             # numbered if sequential, flat if independent
```
