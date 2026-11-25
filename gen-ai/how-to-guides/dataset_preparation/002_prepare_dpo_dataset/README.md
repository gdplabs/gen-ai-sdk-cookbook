# Prepare a DPO Dataset

This recipe uses the public `gllm-finetuning` ingestion registry to load and validate a local CSV file, then runs `preprocess()` to filter, render, and format preference pairs for direct preference optimization.

## Run

```bash
./setup.sh
uv run python prepare_dpo_dataset.py
```

On Windows, run `setup.bat` before `uv run python prepare_dpo_dataset.py`.

## Expected Output

```text
Prepared 2 DPO examples.
{'messages': [{'role': 'system', 'content': 'You are an expert Indonesian financial regulation analyst. Answer the question using only the provided context.'}, {'role': 'user', 'content': 'Context: POJK 56/2023 imposes administrative sanctions for late submission of monthly risk reports ranging from written warnings to fines for repeat violations. Question: Is late filing of the monthly risk report penalized?'}], 'chosen': {'role': 'assistant', 'content': 'Yes sanctions range from warnings to fines'}, 'rejected': {'role': 'assistant', 'content': 'The regulation only issues warnings'}}
```

Run `uv run python -m pytest` to execute the recipe smoke test.
