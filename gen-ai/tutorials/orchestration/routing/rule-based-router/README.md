# Rule-Based Router

## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gdplabs/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/tutorials/orchestration/routing/rule-based-router
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
   | `uv run rule_based_router.py` | Keyword/pattern routing across billing, tech_support, sales, faq | [Complete Example](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/routing/rule-based-router#complete-example) |

## 📝 Notes

- **No credentials required.** Rule-based routing is fully deterministic keyword
  matching.
- **`llmrouter` extra:** `gllm-pipeline`'s `router` package eagerly imports the
  classifier backend, which requires PyTorch. The dependency is therefore
  declared as `gllm-pipeline[llmrouter]` so the import resolves, even though
  rule-based routing itself uses no ML model.

## 📚 Reference

These examples are based on the [GL SDK GitBook documentation](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/routing/rule-based-router).
