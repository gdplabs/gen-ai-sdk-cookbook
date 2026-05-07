## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../README.md).

## 📂 Project Setup

The folder structure for this example:

```
pipeline-step-exclusion/
├── pipeline.py
├── pyproject.toml
├── .env.example
├── .python-version
├── setup.sh
└── setup.bat
```

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
   Full pipeline result
   Current exclusions: []
   Report: {'sentiment': 'positive', 'topics': ['pipelines', 'feature-flags', 'debugging'], 'entities': [], 'language': 'skipped'}
   Without sentiment
   Current exclusions: ['sentiment']
   Report: {'sentiment': 'skipped', 'topics': ['pipelines', 'feature-flags', 'debugging'], 'entities': [], 'language': 'skipped'}
   Conditional pipeline after excluding the detailed branch
   Current exclusions: ['conditional_analysis.true']
   Conditional result keys: ['extracted_text', 'input_document']
   Adaptive pipeline
   Current exclusions: ['analysis_parallel.sentiment', 'analysis_parallel.topics', 'analysis_parallel.language']
   Report: {'sentiment': 'skipped', 'topics': [], 'entities': ['GL SDK', 'Feature Flags'], 'language': 'skipped'}
   Lifecycle start: []
   After exclude: ['analysis_parallel.sentiment', 'analysis_parallel.topics']
   After include: ['analysis_parallel.topics']
   Excluded steps: []
   After clear: []
   ```

## 📚 Reference

These examples are based on the [GL SDK GitBook documentation](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/guides/build-end-to-end-rag-pipeline/pipeline-step-exclusion).
