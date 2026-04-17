# Few-Shot Experiment (Metric-Level)

A standalone experiment runner for evaluating LLM responses using gllm-evals SDK with metric-level few-shot examples.

## Overview

This experiment uses direct `metric.evaluate()` calls with the `temp_fewshot` parameter to provide **metric-level few-shot examples**. Each question gets its own few-shot examples for each metric (completeness, redundancy, groundedness).

## Features

- **Metric-level few-shot**: Direct `metric.evaluate()` calls with `temp_fewshot` parameter
- **CLI configuration**: All parameters configurable via command-line arguments
- **Multiple metrics**: Completeness, Redundancy, Groundedness
- **Parallel processing**: Async evaluation with configurable workers
- **Question filtering**: Evaluate specific question IDs or all questions
- **CSV export**: Results saved with detailed metrics and relevance ratings

## Requirements

- Python 3.11+ (<=3.13)
- `gcloud` CLI ([installation guide](https://cloud.google.com/sdk/docs/install))
- GCP authentication via `gcloud auth login`
- Access to GDPLabs internal package index (`https://glsdk.gdplabs.id/gen-ai-internal/`)
- API credentials (Google, Anthropic, etc.)

## Installation

This experiment is **fully standalone** and can be shared with other developers. It installs `gllm-evals` from the internal package index using gcloud authentication.

```bash
# 1. Authenticate with gcloud
gcloud auth login

# 2. Install dependencies with authenticated access
make install

# Or manually:
pip install --extra-index-url "https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-evals[deepeval,langchain,ragas]" pandas python-dotenv
```

**Note**: The experiment uses gcloud OAuth tokens to access the internal package index at `https://glsdk.gdplabs.id/gen-ai-internal/`. You must be authenticated with GCP.

## Configuration

Create a `.env` file or set environment variables:

```bash
# Copy example env file
cp .env.example .env

# Edit and add your API key
export GOOGLE_API_KEY="your-api-key"
# or
export ANTHROPIC_API_KEY="your-api-key"
```

## Usage

### Basic Usage

```bash
# Run with default settings (first experiment, all questions)
python experiment_fewshot.py

# Specify evaluation model
python experiment_fewshot.py --eval-model google/gemini-3-flash-preview

# Filter specific question IDs
python experiment_fewshot.py --question-ids 1 2 5 10

# Adjust parallel workers
python experiment_fewshot.py --workers 10
```

### Advanced Usage

```bash
# Run specific experiment with custom output
python experiment_fewshot.py \
  --experiment-index botanica \
  --eval-model anthropic/claude-3.5-sonnet \
  --workers 8 \
  --question-ids 1 2 3 \
  --output-dir ./results

# Use small dataset for testing
python experiment_fewshot.py --use-small-data

# Custom few-shot examples file
python experiment_fewshot.py --fewshot-json ./custom_fewshot.json
```

### Available Arguments

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--experiment-index` | int | 0 | Index of experiment to run (0-14) |
| `--eval-model` | str | google/gemini-3-flash-preview | Model for evaluation |
| `--workers` | int | 5 | Number of parallel workers |
| `--question-ids` | int[] | None | Specific question IDs to evaluate (None = all) |
| `--use-small-data` | flag | False | Use small dataset for testing |
| `--fewshot-json` | str | auto | Path to few-shot examples JSON |
| `--output-dir` | str | ./output | Output directory for results |
| `--fewshot-mode` | str | replace | Mode for few-shot: 'append' or 'replace' |

## Output

Results are saved to CSV files with the following structure:

```
output/
├── experiment_0_qids_1_2_3.csv    # Evaluation results
└── experiment_0_summary.json      # Experiment summary
```

### Output Columns

- `question_id`: Question identifier
- `question`: Original question text
- `generated_response`: Model's response
- `retrieved_context`: Context provided to model
- `expected_response`: Ground truth response
- `predicted_completeness`: Completeness score (1-3)
- `completeness_reason`: Explanation for score
- `predicted_redundancy`: Redundancy score (1-3)
- `redundancy_reason`: Explanation for score
- `predicted_groundedness`: Groundedness score (1-3)
- `groundedness_reason`: Explanation for score
- `autoeval_rr`: Overall relevance rating (Good/Acceptable/Bad)

## Few-Shot JSON Format

The few-shot examples JSON should follow this structure:

```json
{
  "1": {
    "fewshot_completeness": "Example: Input: ...\nActual Output: ...\nScore: 3\nReason: ...",
    "fewshot_redundancy": "Example: Input: ...\nActual Output: ...\nScore: 1\nReason: ...",
    "fewshot_groundedness": "Example: Input: ...\nActual Output: ...\nScore: 3\nReason: ...",
    "retrieved_context": "Context for this question..."
  },
  "2": {
    ...
  }
}
```

## Examples

### Run Quick Test

```bash
# Test with single question
make test

# Or manually
python experiment_fewshot.py --question-ids 1 --workers 2
```

### Run Full Experiment

```bash
# Run all experiments sequentially
make run-all

# Or run specific experiments
python experiment_fewshot.py --experiment-index 0
python experiment_fewshot.py --experiment-index botanica
python experiment_fewshot.py --experiment-index 2
```

### Run with Different Models

```bash
# Google Gemini
python experiment_fewshot.py --eval-model google/gemini-3-flash-preview

# Anthropic Claude
python experiment_fewshot.py --eval-model anthropic/claude-3.5-sonnet

# OpenAI GPT-4
python experiment_fewshot.py --eval-model openai/gpt-4
```

## Makefile Commands

```bash
make install      # Install dependencies
make test         # Run quick test with 1 question
make run          # Run default experiment
make run-all      # Run all experiments
make clean        # Clean output files
make lint         # Run code quality checks
```

## Differences from Legacy Approach

This modern implementation differs from the legacy notebook-based approach:

1. **No Voting Mechanism**: Single evaluation per row (no majority voting)
2. **No Retry Logic**: No automatic retry until 100% alignment
3. **Metric-Level Few-Shot**: Uses `temp_fewshot` parameter in `metric.evaluate()`
4. **CLI-Based**: All configuration via command-line arguments
5. **Standalone**: Self-contained folder with all dependencies
6. **Simpler**: Focused on core evaluation functionality

## Architecture

```
experiment_fewshot.py          # Main script
├── config.py                  # Experiment configurations
├── evaluator.py               # Evaluation logic with metric.evaluate()
├── utils.py                   # Helper functions
└── data/
    └── fewshot_examples.json  # Few-shot examples per question
```

## How It Works

1. **Load Data**: Load experiment CSV and few-shot JSON
2. **Evaluate Rows**: For each row, call `metric.evaluate()` with `temp_fewshot` parameter
3. **Parallel Processing**: Use asyncio with configurable workers for concurrent evaluation
4. **Calculate Rating**: Aggregate metric scores into relevance rating (Good/Acceptable/Bad)
5. **Save Results**: Export to CSV and JSON with all metrics and reasons

## Troubleshooting

### GCloud Authentication Issues

```bash
# Check if authenticated
gcloud auth list

# Login if needed
gcloud auth login

# Verify access token generation
gcloud auth print-access-token

# If using application default credentials
gcloud auth application-default login
```

### Package Index Access Issues

```bash
# Verify access to internal package index
curl -I https://glsdk.gdplabs.id/gen-ai-internal/simple/

# Test authenticated access
curl -H "Authorization: Bearer $(gcloud auth print-access-token)" https://glsdk.gdplabs.id/gen-ai-internal/simple/

# If behind VPN or firewall, ensure network access to GDPLabs infrastructure
```

### API Key Issues

```bash
# Verify API key is set
echo $GOOGLE_API_KEY

# Set API key in .env file or export
export GOOGLE_API_KEY="your-key"
```

### Memory Issues

```bash
# Reduce workers if running out of memory
python experiment_fewshot.py --workers 2

# Or run fewer questions at once
python experiment_fewshot.py --question-ids 1 2 3
```

### Missing Few-Shot Data

```bash
# Verify few-shot JSON exists
ls data/fewshot_examples.json

# Specify custom path
python experiment_fewshot.py --fewshot-json /path/to/fewshot.json
```

## Contributing

To add new experiments:

1. Update `EXPERIMENTS` list in `config.py`
2. Ensure CSV files exist in expected paths
3. Test with `--use-small-data` first

## License

Internal use only.
