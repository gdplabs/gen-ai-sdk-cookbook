# Prepare an SFT Dataset

This recipe uses the public `gllm-finetuning` ingestion registry to load and validate a local CSV file, then runs `preprocess()` to filter, render, and format it for supervised fine-tuning.

## Run

```bash
./setup.sh
uv run python prepare_sft_dataset.py
```

On Windows, run `setup.bat` before `uv run python prepare_sft_dataset.py`.

## Expected Output

```text
Prepared 2 SFT examples.
{'messages': [{'role': 'system', 'content': 'You are a precise support assistant. Answer only from the supplied context.'}, {'role': 'user', 'content': 'Context: A data warehouse centralizes historical data from operational systems for analytics.\n\nQuestion: What does a data warehouse store?'}, {'role': 'assistant', 'content': 'A data warehouse stores integrated historical data for reporting and analysis.'}]}
```

Run `uv run python -m pytest` to execute the recipe smoke test.
