## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../README.md).

## 📂 Project Setup

If you have downloaded the Complete Guide Files, you can proceed to the next step. This is the folder structure:

```
rag-with-dynamic-models/
├── data/
│   ├── <index>/...
│   ├── chroma.sqlite3
│   ├── imaginary_animals.csv
├── .env
├── pipeline.py
└── pyproject.toml
```

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gdplabs/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/how-to-guides/build_end_to_end_rag_pipeline/012_rag_with_dynamic_models
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
    Model: openai/gpt-5-nano
    Response: I don't have your dataset. If you share the data (or describe its structure), I can pull out the nocturnal creatures...
    ```

## 📚 Reference

These examples are based on the [GL SDK GitBook documentation](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/guides/build-end-to-end-rag-pipeline/rag-with-dynamic-models).
