## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gdplabs/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/how-to-guides/build_end_to_end_rag_pipeline/010_pipeline_step_exclusion
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

   ```bash
   uv run pipeline.py
   ```

4. **Expected Output**

   ```text
   Full pipeline
   Current exclusions: []
   Report: {'sentiment': 'positive', 'topics': ['pipelines', 'feature-flags', 'debugging'], 'language': 'en'}
   After excluding the topics branch
   Current exclusions: ['analysis_parallel.topics']
   Report: {'sentiment': 'positive', 'topics': [], 'language': 'en'}
   After excluding the entire parallel block
   Current exclusions: ['analysis_parallel']
   Report: {'sentiment': 'skipped', 'topics': [], 'language': 'skipped'}
   After clearing exclusions
   Current exclusions: []
   Report: {'sentiment': 'positive', 'topics': ['pipelines', 'feature-flags', 'debugging'], 'language': 'en'}
   ```

## 📚 Reference

These examples are based on the [GL SDK GitBook documentation](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/guides/build-end-to-end-rag-pipeline/pipeline-step-exclusion).
