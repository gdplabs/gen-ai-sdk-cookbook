## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gdplabs/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/how-to-guides/build_end_to_end_rag_pipeline/009_parallel_pipeline_processing
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
   uv run parallel_pipeline.py
   ```

4. **Expected Output**

   ```text
   Sequential pipeline duration: 1.18s
   Sequential pipeline report: {'sentiment': 'positive', 'topics': ['pipelines', 'parallelism', 'observability'], 'entities': ['GL SDK', 'LangGraph'], 'language': 'en'}
   Parallel pipeline duration: 0.39s
   Parallel pipeline report: {'sentiment': 'positive', 'topics': ['pipelines', 'parallelism', 'observability'], 'entities': ['GL SDK', 'LangGraph'], 'language': 'en'}
   Equivalent report: True
   Speedup: 3.06x
   ```

## 📚 Reference

These examples are based on the [GL SDK GitBook documentation](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/guides/build-end-to-end-rag-pipeline/parallel-pipeline-processing).
