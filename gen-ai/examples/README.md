# Gen AI SDK — Examples

All examples are self-contained. Each folder has its own `README.md`, `.env.example`, and setup scripts.

Structure mirrors the [GL Generative AI documentation](https://docs.gdplabs.id/gen-ai-sdk).

## Guides

Goal-oriented examples that walk through a complete task end-to-end.

| Example | Level | Topic | Docs |
|---|---|---|---|
| [guides/build_end_to_end_rag_pipeline](./guides/build_end_to_end_rag_pipeline/) | Beginner → Advanced | RAG, Pipeline, Routing, Guardrails, Caching | [Build End-to-End RAG Pipeline](https://docs.gdplabs.id/gen-ai-sdk/guides/build-end-to-end-rag-pipeline) |
| [guides/a2ui](./guides/a2ui/) | Intermediate | UI integration, Next.js, Vite | — |

## Tutorials

Component-level deep dives, organized by SDK module.

### Inference

| Example | Level | Topic | Docs |
|---|---|---|---|
| [tutorials/inference/lm_invoker](./tutorials/inference/lm_invoker/) | Beginner | LM Invoker, Model switching, System prompts | [Language Model Invoker](https://docs.gdplabs.id/gen-ai-sdk/tutorials/inference/lm-invoker) |
| [tutorials/inference/lm_request_processor](./tutorials/inference/lm_request_processor/) | Intermediate | Streaming, Structured output, Tool calling | [LM Request Processor](https://docs.gdplabs.id/gen-ai-sdk/tutorials/inference/lm-request-processor) |
| [tutorials/inference/realtime_session](./tutorials/inference/realtime_session/) | Advanced | Realtime, Text, Audio, Tool calling | [Realtime Session](https://docs.gdplabs.id/gen-ai-sdk/tutorials/inference/realtime-session) |

### Data Store

| Example | Level | Topic | Docs |
|---|---|---|---|
| [tutorials/data_store](./tutorials/data_store/) | Intermediate | Vector indexing, Metadata filtering | [Data Store](https://docs.gdplabs.id/gen-ai-sdk/tutorials/data-store) |

### Evaluation

| Example | Level | Topic | Docs |
|---|---|---|---|
| [tutorials/evaluation](./tutorials/evaluation/) | Intermediate | Evaluation, Custom scorers, LLM-as-a-judge | [Evaluation](https://docs.gdplabs.id/gen-ai-sdk/tutorials/evaluation) |

### Core

| Example | Level | Topic | Docs |
|---|---|---|---|
| [tutorials/core/custom_component](./tutorials/core/custom_component/) | Advanced | Custom components, Extensibility | [Component](https://docs.gdplabs.id/gen-ai-sdk/tutorials/core/component) |

### Generation

| Example | Level | Topic | Docs |
|---|---|---|---|
| [deep_researcher](./deep_researcher/) | Intermediate | Deep research, Multi-provider | [Deep Researcher](https://docs.gdplabs.id/gen-ai-sdk/tutorials/generation/deep-researcher) |

> `deep_researcher` will move to `tutorials/generation/deep_researcher` in a follow-up PR.

## Where to Start

New to the SDK? Start with `tutorials/inference/lm_invoker/lm_invoker_basic_usage/`, then work through `guides/build_end_to_end_rag_pipeline/` in numbered order.
