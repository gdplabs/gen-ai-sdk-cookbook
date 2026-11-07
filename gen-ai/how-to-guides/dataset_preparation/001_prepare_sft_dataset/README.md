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
{'messages': [{'role': 'system', 'content': 'You are an expert Indonesian financial regulation analyst. Answer the question using only the provided context.'}, {'role': 'user', 'content': 'Context: OJK Regulation POJK 12/2020 requires rural banks (BPR) to maintain minimum core capital of IDR 6 billion by end 2024 with staged increases announced in advance. Question: What is the minimum capital requirement for a rural bank?'}, {'role': 'assistant', 'content': 'IDR 6 billion'}]}
```

Run `uv run python -m pytest` to execute the recipe smoke test.
