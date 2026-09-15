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
{'messages': [{'role': 'system', 'content': 'You are a precise support assistant. Answer only from the supplied context.'}, {'role': 'user', 'content': 'Context: Passwords must be protected with a slow salted password hash.\n\nQuestion: How should a password be stored?'}], 'chosen': {'role': 'assistant', 'content': 'Store passwords with a unique salt and a slow password-hashing algorithm.'}, 'rejected': {'role': 'assistant', 'content': 'Store encrypted passwords in a shared configuration file.'}}
```

Run `uv run python -m pytest` to execute the recipe smoke test.
