# Evaluate Suites — Google Sheets Data Source

This example demonstrates how to use **`evaluate_suites()`** with data loaded from Google Sheets spreadsheets.

Each suite pulls its dataset from a **different worksheet** in the same spreadsheet, enabling you to organize test cases by domain or evaluation strategy.

## Prerequisites

- Python 3.11 or higher
- Google Cloud SDK (gcloud CLI) installed
- Google AI API Key
- Google Sheets API enabled with service account credentials

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
make run        # Run the evaluate_suites from Google Sheets script
make clean      # Clean up generated files
```
