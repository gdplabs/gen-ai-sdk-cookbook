# Custom Prompts: fewshot + additional_info Split

This tutorial demonstrates how to use the new `fewshot` and `additional_info` constructor parameters to customize evaluation prompts per row via CSV columns.

Previously, both were bundled into a single `additional_context` parameter. The split gives you finer control and clearer semantics.

## How It Works

| Step | Description |
|------|-------------|
| 1 | Load test cases from `data/banking_eval_data.csv` via `DictDataset.from_csv` |
| 2 | CSV columns `temp_fewshot_completeness`, `temp_fewshot_completeness_mode`, and `temp_info_completeness` override constructor defaults per row |
| 3 | `EvalSuite` wraps the data with a `GEvalGenerationEvaluator` |
| 4 | `evaluate_suites()` runs the suite and returns results as JSON |

## CSV Column Reference

| Column | Purpose |
|--------|---------|
| `temp_fewshot_{metric_name}` | Per-row few-shot examples |
| `temp_fewshot_{metric_name}_mode` | `"append"` (default) or `"replace"` |
| `temp_info_{metric_name}` | Per-row domain info |
| `evaluation_step_{metric_name}` | Per-row evaluation steps |
| `fewshot_{metric_name}` | **Deprecated** — use `temp_fewshot_{metric_name}` instead |

## Sample CSV Data

The example uses `data/banking_eval_data.csv`:

| input | expected_output | actual_output | temp_fewshot_completeness | temp_fewshot_completeness_mode | temp_info_completeness |
|-------|-----------------|---------------|---------------------------|--------------------------------|------------------------|
| What is KYC? | KYC is Know Your Customer verification | KYC verifies customer identity | KYC-specific: Must include identity verification steps | append | KYC requires government-issued ID and proof of address. |
| What is compliance? | Following laws and regulations | Compliance means following rules | | | Compliance in banking includes AML, KYC, and SAR reporting. |
| What is SWIFT? | SWIFT is international payment messaging | SWIFT sends international payments | SWIFT-specific: Focus on international banking | replace | |

- **Row 1**: Appends per-row fewshot to the constructor default, adds per-row domain info
- **Row 2**: Only overrides domain info; fewshot uses constructor default
- **Row 3**: Replaces constructor fewshot entirely with per-row fewshot

## Prerequisites

- Python 3.11 or higher
- Google Cloud SDK (gcloud CLI) installed
- A Google API Key

## Installation

### 1. Authenticate with Google Cloud

```bash
gcloud auth login
```

### 2. Install Dependencies

Using `uv` (recommended):

```bash
make install
```

### 3. Set Up Environment Variables

```bash
cp .env.example .env
# Edit .env with your API key
```

## Usage

```bash
make run
```

## Available Make Commands

```bash
make help       # List all commands
make install    # Install dependencies
make run        # Run the custom prompts example
make clean      # Clean up generated files
```
