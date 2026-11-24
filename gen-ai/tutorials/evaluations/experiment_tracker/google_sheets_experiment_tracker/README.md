# Google Sheets Experiment Tracker Tutorial

Use `GoogleSheetsExperimentTracker` to save an evaluation run in Google Sheets. Run the same dataset twice to compare the scores on a shared leaderboard.

## Prerequisites

- Python 3.12 or 3.13
- An OpenRouter API key for the evaluation judge
- A Google Cloud service account with the **Google Sheets API** and **Google Drive API** enabled
- Your target Google Sheet (or Drive folder) shared with the service account email as an **Editor**

## Installation

### 1. Install dependencies

With `uv` and Make installed, run:

```bash
make install
```

Or install dependencies in an active Python 3.12 or 3.13 environment:

```bash
pip install "gllm-evals-binary>=0.1.45,<0.2.0" "python-dotenv>=1.0.0,<2.0.0"
```

### 2. Set up environment variables

```bash
cp .env.example .env
```

Set `OPENROUTER_API_KEY` for the judge and `GOOGLE_SHEETS_CLIENT_EMAIL` to the service account email. For `GOOGLE_SHEETS_PRIVATE_KEY`, base64-encode the PEM text in the service account JSON's `private_key` field, including its line breaks. Paste the single-line base64 value into `.env`.

Set `GOOGLE_SHEETS_SPREADSHEET_ID` to write to an existing spreadsheet. To find or create a spreadsheet named `my_evals` in a Drive folder, set `MASTER_DRIVE_FOLDER_ID` and leave the spreadsheet ID blank.

## Usage

Run the Google Sheets experiment tracker example:

```bash
make run
```

Open the printed run worksheet link to inspect the five rows. Run `make run` again with the same target. Open the printed leaderboard link and compare the scores for the two run IDs.

If you installed with pip, run `python example_google_sheets_experiment_tracker.py` in the same environment.

## Available Make Commands

```bash
make install    # Install dependencies using uv
make run        # Run the Google Sheets experiment tracker script
make clean      # Clean up generated files
```
