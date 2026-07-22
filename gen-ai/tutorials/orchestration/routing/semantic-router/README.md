# Semantic Router

## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gdplabs/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/tutorials/orchestration/routing/semantic-router
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

3. **Run the examples**

   | Script | Description | GitBook Section |
   |--------|-------------|-----------------|
   | `uv run native_backend.py` | Native backend quickstart (`SemanticRouter.native`) + route filtering | [Quickstart → Native Backend](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/routing/semantic-router#option-1-native-backend) |
   | `uv run aurelio_em_invoker.py` | Aurelio backend with an EM Invoker passed directly (auto-wrapped) | [Aurelio Backend with EM Invoker](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/routing/semantic-router/aurelio-backend#em-invoker-encoder) |
   | `uv run aurelio_em_encoder.py` | Aurelio backend with an explicit `EMInvokerEncoder` | [Aurelio Backend with EM Invoker Encoder](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/routing/semantic-router/aurelio-backend#em-invoker-encoder) |
   | `uv run knn_backend.py` | KNN backend (`SemanticRouter.knn`) — see note below | [Quickstart → KNN Backend](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/routing/semantic-router#option-4-knn-backend) |
   | `uv run presets.py` | `from_preset` API + bundled presets in the installed SDK — see note below | [Using Presets](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/routing/semantic-router#using-presets) |
   | `uv run complete_example.py` | End-to-end native routing over billing / tech_support / faq | [Complete Example](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/routing/semantic-router#complete-example) |

## 📝 Notes

- **Embeddings are stubbed.** `fake_em.py` provides a deterministic offline
  `FakeEMInvoker` (a real `BaseEMInvoker` subclass, so both the native backend
  and the Aurelio auto-wrap accept it). It embeds text with a stemmed,
  stopword-filtered hashing bag-of-words so cosine similarity is driven by
  content words. Each script's docstring shows the real `build_em_invoker`
  construction. The `SemanticRouter`, its backends, and the Aurelio Labs
  `semantic-router` library are the real code path.
- `similarity_threshold` is `0.2` here, tuned for the sparse stub embeddings.
  With a real embedding model, `0.5` (the GitBook default) is the recommended
  starting point.
- **`knn_backend.py` is blocked on a data artifact.** `SemanticRouter.knn`
  needs a pre-trained KNeighborsClassifier `.pkl`. None ships with the SDK or
  this cookbook, so the script constructs the `KNNConfig` (validates offline)
  and reports the missing model rather than fabricating one.
- **`presets.py` — the GitBook text preset is not bundled.** The only preset in
  the installed `gllm-pipeline` is `(ModalityType.IMAGE, "domain_specific")`,
  which needs a live multimodal model. The script documents the `from_preset`
  API and prints the bundled presets. For runnable routing, use the explicit
  `route_examples` scripts above.
- **`llmrouter` extra:** required because `gllm-pipeline`'s `router` package
  eagerly imports the classifier backend (PyTorch).

## 📚 Reference

These examples are based on the [GL SDK GitBook documentation](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/routing/semantic-router).
