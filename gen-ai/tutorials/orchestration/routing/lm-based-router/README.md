# LM-Based Router

## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gdplabs/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/tutorials/orchestration/routing/lm-based-router
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
   | `uv run lm_based_router.py` | LM-driven routing across billing, tech_support, sales, general | [Complete Example](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/routing/lm-based-router#complete-example) |

## 📝 Notes

- **LM call is stubbed.** To run offline without an API key, the live LM
  request processor is replaced with a small deterministic `StubLMRequestProcessor`.
  The script's docstring shows the real `build_lm_request_processor` construction
  you would use in production. The `LMBasedRouter`, route extraction, validation,
  and `route_filter` are all exercised as the real library code path.
- **`llmrouter` extra:** required because `gllm-pipeline`'s `router` package
  eagerly imports the classifier backend (PyTorch).

## 📚 Reference

These examples are based on the [GL SDK GitBook documentation](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/routing/lm-based-router).
