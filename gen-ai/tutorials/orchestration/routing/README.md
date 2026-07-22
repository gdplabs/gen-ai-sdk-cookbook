# Routing

Runnable cookbook examples for the GL SDK router types. A router selects which
downstream path (tool, retriever, prompt, agent) handles a given query.

Each subdirectory is a self-contained `uv` project with its own setup scripts,
README, and runnable script(s).

| Router | Directory | Runs offline? |
|--------|-----------|---------------|
| Rule-Based Router | [`rule-based-router/`](rule-based-router/) | ✅ deterministic, no credentials |
| LM-Based Router | [`lm-based-router/`](lm-based-router/) | ✅ LM call stubbed |
| Similarity-Based Router | [`similarity-based-router/`](similarity-based-router/) | ✅ embeddings stubbed |
| Semantic Router | [`semantic-router/`](semantic-router/) | ✅ native + Aurelio (KNN/presets: see dir notes) |
| Classifier Router | [`classifier-router/`](classifier-router/) | ⚠️ needs a pre-trained model file |

> **Note on stubs:** Examples that would otherwise need live OpenAI/LM
> credentials replace only the external embedding/LM call with a deterministic
> offline stub, so they run in CI without secrets. Every stub is documented in
> the directory's README, and each script's docstring shows the real
> `build_em_invoker` / `build_lm_request_processor` construction. The routers
> themselves are always the real library code path.

## 📚 Reference

Based on the [GL SDK GitBook documentation](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/routing).
