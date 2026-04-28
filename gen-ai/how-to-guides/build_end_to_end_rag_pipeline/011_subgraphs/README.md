## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../README.md).

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gdplabs/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/how-to-guides/build_end_to_end_rag_pipeline/011_subgraphs
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
   uv run pipeline_builder.py
   ```

4. **Expected Output**

   ```text
   Processed query: what are some forest animals?
   Expanded query: what are some forest animals? | focus: forest animals
   Final response: Forest animals mentioned in the retrieved context: Luminafox, Dusk Panther, and Bramble Owl.
   Metadata: {'response_length': 92, 'source_count': 3, 'context_preview': 'Luminafox lives in moonlit forests and is active at night. D'}
   ```

## 📚 Reference

These examples are based on the [GL SDK GitBook documentation](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/guides/build-end-to-end-rag-pipeline/subgraphs).
