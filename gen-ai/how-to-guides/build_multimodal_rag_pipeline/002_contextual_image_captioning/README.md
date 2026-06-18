## ⚙️ Prerequisites

Please refer to prerequisites [here](../../../README.md).

## Overview

This example extends the [basic image search pipeline](../001_image_search_pipeline) by adding **contextual image captioning**.

In the base pipeline, images are captioned using only the image itself. Here, the indexer also collects the body text from the same PDF section as the image and passes it as `text_context` to `LMBasedImageToCaption`. This gives the language model the article context it needs to generate captions that are grounded in the surrounding content — rather than describing the image in isolation.

### How it works

The PDF is structured as a series of articles, each with:
1. A heading
2. An image
3. Body paragraphs

The indexer groups all elements by their heading metadata to identify which section each element belongs to. For every image element, it concatenates the non-image text from the same section and passes it as `text_context` when calling `caption_converter.convert()`.

```
Section key (from heading metadata)
        │
        ▼
┌─────────────────────────────┐
│  Body text (concatenated)   │  ← text_context
└─────────────────────────────┘
        │
        ▼
LMBasedImageToCaption.convert(image_bytes, text_context=...)
        │
        ▼
Contextually grounded caption
```

## 🚀 Getting Started

1. **Clone the repository & open the directory**

   ```bash
   git clone https://github.com/gl-sdk/gen-ai-sdk-cookbook.git
   cd gen-ai-sdk-cookbook/gen-ai/how-to-guides/build_multimodal_rag_pipeline/002_contextual_image_captioning
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

3. **Prepare `.env` file**
   Copy `.env.example` to `.env` and fill in your credentials.
   ```env
   EMBEDDING_MODEL="gemini-embedding-001"
   LANGUAGE_MODEL="google/gemini-3-flash-preview"
   DEFAULT_IMAGE_CAPTIONING_MODEL_ID="google/gemini-2.5-flash"
   GOOGLE_API_KEY="..."
   ```

4. **Index the document**

   ```bash
   uv run indexer.py
   ```

5. **Run the pipeline**

   ```bash
   uv run pipeline.py
   ```

## 🚀 Reference

These examples are based on the [GL SDK Gitbook documentation How-to-Guide page](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/guides/build-multimodal-rag-pipeline/image-search-pipeline).
