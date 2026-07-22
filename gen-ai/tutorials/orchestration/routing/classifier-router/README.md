# Classifier Router

## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gdplabs/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/tutorials/orchestration/routing/classifier-router
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
   | `uv run classifier_router.py` | Builds `MLPConfig`/`SVMConfig`; reports the required trained model — see note | [Quickstart](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/routing/classifier-router#quickstart) |

## 📝 Notes

- **Blocked on a data artifact.** `ClassifierRouter.mlp(...)` / `.svm(...)`
  require a **pre-trained** classifier model file (`.pkl` for sklearn, `.pt` for
  PyTorch) trained on your routing labels. No such model ships with the SDK or
  this cookbook, so `model_path` has nothing to point at. The script builds the
  configs (which validate offline) and reports the missing model rather than
  fabricating one. Train a classifier on representative labeled data, then wire
  `model_path` per the GitBook page to enable live routing.
- **`llmrouter` extra:** `gllm-pipeline[llmrouter]` pulls in PyTorch and
  scikit-learn, required for classifier inference.

## 📚 Reference

These examples are based on the [GL SDK GitBook documentation](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration/routing/classifier-router).
