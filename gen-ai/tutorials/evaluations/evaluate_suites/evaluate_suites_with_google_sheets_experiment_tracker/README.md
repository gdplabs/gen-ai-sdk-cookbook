# Evaluate Suites — Google Sheets Experiment Tracker

This example demonstrates how to use **`evaluate_suites()`** with **`GoogleSheetsExperimentTracker`** to write evaluation results directly to a Google Spreadsheet.

The script uses built-in datasets from `gllm-evals-binary` and sends all results (experiment rows + leaderboard) to Google Sheets instead of CSV.

## Prerequisites

- Python 3.12 or higher
- An OpenRouter API Key for the DeepSeek judge model
- Google Sheets API enabled with service account credentials

## Installation

### 1. Install Dependencies

```bash
make install
```

### 2. Set Up Environment Variables

```bash
cp .env.example .env
# Edit .env with your OpenRouter API key and Google Sheets service account credentials
```

## Usage

```bash
make run
```

## Available Make Commands

```bash
make install    # Install dependencies using uv
make run        # Run the evaluate_suites script
make clean      # Clean up generated files
```
