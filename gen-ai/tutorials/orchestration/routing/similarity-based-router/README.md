# Similarity-Based Router

> **Deprecated:** `SimilarityBasedRouter` is superseded by `SemanticRouter.native()`
> in v0.5. This example (and the GitBook page) already use `SemanticRouter.native()`.

## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gdplabs/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/tutorials/orchestration/routing/similarity-based-router
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

3. **Run the example**

   | Script | Description | GitBook Section |
   |--------|-------------|-----------------|
   | `uv run similarity_based_router.py` | Embedding-similarity routing across billing, tech_support, sales, faq | [Complete Example](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/routing/similarity-based-router#complete-example) |

## 📝 Notes

- **Embeddings are stubbed.** `fake_em.py` provides a deterministic hashing
  bag-of-words `FakeEMInvoker` so the example runs offline without OpenAI
  credentials. The script docstring shows the real `build_em_invoker`
  construction. The `SemanticRouter` and its similarity backend are the real
  library code path.
- `similarity_threshold` is set to `0.3` here because the stub embeddings are
  sparser than a real model; with a real embedding model, `0.5` (the GitBook
  default) is the recommended starting point.
- **`llmrouter` extra:** required because `gllm-pipeline`'s `router` package
  eagerly imports the classifier backend (PyTorch).

## 📚 Reference

These examples are based on the [GL SDK GitBook documentation](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/routing/similarity-based-router).
