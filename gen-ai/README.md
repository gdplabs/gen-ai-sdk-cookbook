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
| Build a RAG pipeline step by step | [`build_end_to_end_rag_pipeline/`](./examples/build_end_to_end_rag_pipeline/) |
| Learn how to call a language model | [`lm_invoker/`](./examples/lm_invoker/) |
| Add streaming, structured output, or tool calling | [`lm_request_processor/`](./examples/lm_request_processor/) |
| Connect a vector or SQL data store | [`data_store/`](./examples/data_store/) |
| Evaluate my pipeline | [`evaluation/`](./examples/evaluation/) |
| Add deep research capability | [`deep_researcher/`](./examples/deep_researcher/) |
| Add realtime voice interaction | [`realtime_session/`](./examples/realtime_session/) |
| Build a custom pipeline component | [`custom_component/`](./examples/custom_component/) |

Full index with skill levels and docs links: [`examples/README.md`](./examples/README.md)

## 📁 Example Structure

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
