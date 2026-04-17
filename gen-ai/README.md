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
| Build a RAG pipeline step by step | [`examples/guides/build_end_to_end_rag_pipeline/`](./examples/guides/build_end_to_end_rag_pipeline/) |
| Integrate with a UI (Next.js / Vite) | [`examples/guides/a2ui/`](./examples/guides/a2ui/) |
| Learn how to call a language model | [`examples/tutorials/inference/lm_invoker/`](./examples/tutorials/inference/lm_invoker/) |
| Add streaming, structured output, or tool calling | [`examples/tutorials/inference/lm_request_processor/`](./examples/tutorials/inference/lm_request_processor/) |
| Connect a vector or SQL data store | [`examples/tutorials/data_store/`](./examples/tutorials/data_store/) |
| Evaluate my pipeline | [`examples/tutorials/evaluation/`](./examples/tutorials/evaluation/) |
| Add deep research capability | [`examples/deep_researcher/`](./examples/deep_researcher/) |
| Add realtime voice interaction | [`examples/tutorials/inference/realtime_session/`](./examples/tutorials/inference/realtime_session/) |
| Build a custom pipeline component | [`examples/tutorials/core/custom_component/`](./examples/tutorials/core/custom_component/) |

Full index with skill levels and docs links: [`examples/README.md`](./examples/README.md)

## 📁 Example Structure

Examples are organized to mirror the [GL Generative AI documentation](https://docs.gdplabs.id/gen-ai-sdk):

```
examples/
├── guides/          # goal-oriented walkthroughs (mirrors docs/guides)
└── tutorials/       # component deep dives (mirrors docs/tutorials)
    ├── core/
    ├── data_store/
    ├── evaluation/
    ├── inference/
    └── ...
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
