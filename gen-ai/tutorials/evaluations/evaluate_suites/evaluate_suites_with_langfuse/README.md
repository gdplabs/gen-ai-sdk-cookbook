# Evaluate Suites — Langfuse Experiment Tracker

This example demonstrates how to use **`evaluate_suites()`** with **Langfuse** experiment tracking and custom column mapping.

All suites share a single `LangfuseExperimentTracker` instance with one `mapping` configuration, ensuring consistent logging to Langfuse regardless of which suite a test case belongs to.

## Prerequisites

- Python 3.11 or higher
- Google Cloud SDK (gcloud CLI) installed
- OpenAI API Key
- Langfuse API keys (public + secret)
- Google Sheets API enabled

## Installation

```bash
make install
```

### Set Up Environment Variables

```bash
cp .env.example .env
# Edit .env with your credentials
```

## Usage

```bash
make run
```

## Available Make Commands

```bash
make install    # Install dependencies using uv
make run        # Run the evaluate_suites with Langfuse script
make clean      # Clean up generated files
```
