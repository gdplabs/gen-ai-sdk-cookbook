# Custom Prompts with fewshot and additional_info

This tutorial shows how to customize evaluation prompts using the `fewshot` and `additional_info` constructor parameters, and how to override them per test case via CSV columns.

Use `fewshot` to provide scored examples that anchor the judge's scoring behavior. Use `additional_info` to supply domain rules, compliance standards, or contextual instructions. Both can be set once as constructor defaults and overridden per row in your dataset.

## How It Works

| Step | Description |
|------|-------------|
| 1 | Initialize a metric with constructor-level `fewshot` and `additional_info` as defaults |
| 2 | Load test cases from `data/banking_eval_data.csv` via `DictDataset.from_csv` |
| 3 | CSV columns `temp_fewshot_completeness`, `temp_fewshot_completeness_mode`, and `temp_info_completeness` override the constructor defaults per row |
| 4 | `EvalSuite` wraps the data with a `GEvalGenerationEvaluator` |
| 5 | `evaluate_suites()` runs the suite and returns results as JSON |

## CSV Column Reference

| Column | Purpose |
|--------|---------|
| `temp_fewshot_{metric_name}` | Per-row few-shot examples |
| `temp_fewshot_{metric_name}_mode` | `"append"` (default) or `"replace"` |
| `temp_info_{metric_name}` | Per-row domain info |
| `evaluation_step_{metric_name}` | Per-row evaluation steps |
| `fewshot_{metric_name}` | **Deprecated** — use `temp_fewshot_{metric_name}` instead |

## Test Cases

The example uses `data/banking_eval_data.csv` with three rows, each demonstrating a different override pattern:

| input | expected_output | actual_output | temp_fewshot_completeness | temp_fewshot_completeness_mode | temp_info_completeness |
|-------|-----------------|---------------|---------------------------|--------------------------------|------------------------|
| What is KYC? | KYC is Know Your Customer verification | KYC verifies customer identity | KYC-specific: Must include identity verification steps | append | KYC requires government-issued ID and proof of address. |
| What is compliance? | Following laws and regulations | Compliance means following rules | | | Compliance in banking includes AML, KYC, and SAR reporting. |
| What is SWIFT? | SWIFT is international payment messaging | SWIFT sends international payments | SWIFT-specific: Focus on international banking | replace | |

**Row 1 — append + info override**: The per-row fewshot is appended to the constructor default. Domain info is also overridden. The judge sees both the constructor-level banking examples and the KYC-specific example together.

**Row 2 — info only**: No per-row fewshot; the constructor default applies. Only domain info is overridden with AML/KYC/SAR context specific to compliance questions.

**Row 3 — replace**: The per-row fewshot completely replaces the constructor default. Useful when the constructor example would mislead the judge for this specific question type.

## Expected Output

After running `make run`, you should see a JSON result with per-metric scores for each test case:

```json
{
  "suites": {
    "banking_custom_prompts": {
      "results": [
        {
          "completeness": {
            "score": 0.5,
            "success": true,
            "explanation": "The response identifies KYC as identity verification but omits the regulatory context required in the banking domain (government-issued ID, proof of address). Partially complete.",
            "threshold": 0.5
          },
          "aggregate_success": true
        },
        {
          "completeness": {
            "score": 0.5,
            "success": true,
            "explanation": "The response covers the general definition of compliance but misses the AML, KYC, and SAR specifics required in banking. Partially complete.",
            "threshold": 0.5
          },
          "aggregate_success": true
        },
        {
          "completeness": {
            "score": 1.0,
            "success": true,
            "explanation": "The response correctly identifies SWIFT as an international payment messaging system, which matches the expected output.",
            "threshold": 0.5
          },
          "aggregate_success": true
        }
      ]
    }
  }
}
```

Scores and explanations will vary across runs — LLM judges are stochastic. The key thing to observe is that the judge's reasoning reflects the custom prompts: Row 1 and 2 explanations will reference the banking domain rules from `additional_info`, and Row 3's explanation is shaped by the SWIFT-specific fewshot example that replaced the constructor default.

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
