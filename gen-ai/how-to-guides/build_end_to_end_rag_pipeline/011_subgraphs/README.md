## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../README.md).

## 📂 Project Setup

The folder structure for this example:

```
subgraphs/
├── pipeline_builder.py
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
   Expanded query: what are some forest animals? | focus: nocturnal forest creatures
   Selected documents: ['Glowhopper glimmers in wetland grass and leaves a faint trail of light.', 'Dusk Panther patrols twilight woods and stalks prey after sunset.', 'Luminafox lives in moonlit forests and is active at night.']
   Validated response: Answer: Luminafox, Dusk Panther, and Bramble Owl are highlighted as nocturnal creatures.
   Metadata: {'response_length': 88, 'source_count': 3, 'context_preview': 'Glowhopper glimmers in wetland grass and leaves a faint trai'}
   ```

## 📚 Reference

These examples are based on the [GL SDK GitBook documentation](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/guides/build-end-to-end-rag-pipeline/subgraphs).
