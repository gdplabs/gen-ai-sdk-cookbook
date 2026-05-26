# Tutorial: Temporary Fewshot Per Test Case

This tutorial demonstrates how to use runtime `temp_fewshot`, `temp_info`, and `fewshot_mode` parameters to inject per-call examples and context into evaluation metrics **without** creating new metric classes.

## Concepts

| Parameter | Description |
|-----------|-------------|
| `temp_fewshot` | Inline fewshot example injected at evaluation time |
| `temp_info` | Domain/audience context injected into the evaluation prompt |
| `fewshot_mode` | `"append"` (default) — adds to existing examples; `"replace"` — replaces all existing examples |

## Usage

### Append Mode (default)
```python
await metric.evaluate(data, temp_fewshot="Example: ...", fewshot_mode="append")
```

### Replace Mode
```python
await metric.evaluate(data, temp_fewshot="Example: ...", fewshot_mode="replace")
```

### With Domain Context
```python
await metric.evaluate(data, temp_info="Domain: Finance\nAudience: Regulators")
```

## Priority Rule

Runtime parameters take priority over CSV-level and initialization-level prompts:
**Runtime > CSV > Init**

## Setup

```bash
make install
cp .env.example .env
# Edit .env with your API key
make run
```
