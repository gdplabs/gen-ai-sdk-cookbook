# Metrics Examples

Examples for LLM output evaluation with `gllm-evals`. These cover generation quality, retrieval, prompt alignment, tool use, and multimodal inputs.

The helpfulness and conciseness examples await their SDK implementations. See [Pending SDK Metrics](#pending-sdk-metrics).

## Structure

```
metrics/
├── generation/          # Text generation quality metrics (17 examples, 2 pending)
│   └── dataset_examples/
├── retrieval/           # Retrieval/RAG quality metrics (6 examples)
│   └── dataset_examples/
├── tool_use/            # Tool-use metrics (1 example)
│   └── dataset_examples/
├── multimodal/          # Image-aware evaluation (9 examples)
├── modify_metrics/      # How to modify existing metric attributes (1 example, own project)
└── custom_metric/       # How to create custom metrics (3 approaches, own project)
```

## Prerequisites

- Python >= 3.12
- [uv](https://docs.astral.sh/uv/) package manager
- Access to the internal PyPI index (`gen-ai-internal`)

## Setup

```bash
uv sync
```

Copy `.env.example` to `.env` and add your API key:

```dotenv
OPENROUTER_API_KEY=sk-or-...
```

Every LLM-based example uses DeepSeek V4.1 Flash on OpenRouter (`openrouter/deepseek/deepseek-v4.1-flash-1017`) as its judge model, so `OPENROUTER_API_KEY` is the only key you need.

## Running Examples

```bash
uv run python generation/example_geval_completeness.py
uv run python retrieval/example_top_k_accuracy.py
uv run python tool_use/example_deepeval_tool_correctness.py
```

### Data

The CSV files in each `dataset_examples/` folder use `LLMTestCase` field names (`input`, `actual_output`, `expected_output`, `retrieved_context`, `expected_context`). The loaders (`load_simple_qa_dataset`, `load_simple_rag_dataset`, `load_simple_summarization_dataset`) return `LLMTestCase` rows, so an example reads a row with attribute access, for example `data[0].input`.

---

## Generation Metrics

Evaluate the quality of LLM-generated text. Most examples load data from `generation/dataset_examples/` and print a JSON result.

### DeepEval

| Example | Description |
|---------|-------------|
| `example_deepeval_answer_relevancy.py` | Answer is relevant to the query |
| `example_deepeval_faithfulness.py` | Response stays faithful to retrieved context |
| `example_deepeval_hallucination.py` | Detects hallucinated content |
| `example_deepeval_json_correctness.py` | Validates JSON output against a Pydantic schema |
| `example_deepeval_prompt_alignment.py` | Response follows the prompt instructions |

### G-Eval

| Example | Description |
|---------|-------------|
| `example_geval_completeness.py` | Response completeness vs. expected answer |
| `example_geval_groundedness.py` | Factual grounding in retrieved context |
| `example_geval_language_consistency.py` | Language consistency |
| `example_geval_redundancy.py` | Detects redundant/repetitive content |
| `example_geval_refusal.py` | Evaluates proper refusal behavior |
| `example_geval_refusal_alignment.py` | Refusal alignment with expected behavior |
| `example_geval_summarization_coherence.py` | Summary coherence |
| `example_geval_summarization_consistency.py` | Summary factual consistency |
| `example_geval_summarization_fluency.py` | Summary fluency |
| `example_geval_summarization_relevance.py` | Summary relevance |

### Pending SDK Metrics

The following examples require the pending SDK implementations of `GEvalHelpfulnessMetric` and `GEvalConcisenessMetric`.
These classes are absent from gllm-evals 0.1.41. Run these examples after an SDK release includes these metrics.

| Example | Description |
|---------|-------------|
| `example_geval_helpfulness.py` | Response helpfulness |
| `example_geval_conciseness.py` | Response conciseness |

---

## Retrieval Metrics

Evaluate the quality of retrieved context in RAG pipelines. Examples load data from `retrieval/dataset_examples/`.

### Data Types

| Type | Fields | Used By |
|------|--------|---------|
| `LLMTestCase` | `input`, `actual_output`, `expected_output`, `retrieved_context`, `expected_context` | LLM-based retrieval metrics |
| `RetrievalData` | `retrieved_chunks` (dict of chunk_id → score), `ground_truth_chunk_ids` | Ranking metrics |

### Examples

| Example | Framework | Description |
|---------|-----------|-------------|
| `example_deepeval_contextual_precision.py` | DeepEval | Precision of retrieved chunks |
| `example_deepeval_contextual_recall.py` | DeepEval | Recall of retrieved chunks |
| `example_deepeval_contextual_relevancy.py` | DeepEval | Relevancy of context to query |
| `example_geval_context_sufficiency.py` | G-Eval | Context is sufficient to answer the query |
| `example_pytrec_metric.py` | PyTrec | NDCG, Precision, Recall at k |
| `example_top_k_accuracy.py` | Custom | Top-K hit accuracy |

**Non-LLM metrics** (`example_pytrec_metric.py`, `example_top_k_accuracy.py`) require no API keys.

#### Top-K Accuracy example

```python
data = RetrievalData(
    retrieved_chunks={"chunk_A": 0.95, "chunk_B": 0.88, "chunk_D": 0.65},
    ground_truth_chunk_ids=["chunk_D"],
)
metric = TopKAccuracy(k=[3, 5])
result = await metric.evaluate(data)
# k=3 → 0 (miss), k=5 → 1 (hit)
```

---

## Tool-Use Metrics

| Example | Framework | Description |
|---------|-----------|-------------|
| `example_deepeval_tool_correctness.py` | DeepEval | Agent calls the correct tools with the correct arguments |

The example loads `LLMTestCase` rows with `tools_called` and `expected_tools` from `tool_use/dataset_examples/simple_agent_tool_call_data.json`, and a `tool_schema.json` that defines the available tools (e.g., `calculator`, `weather_search`, `send_email`).

---

## Multimodal

| Folder | Examples | Description |
|--------|---------:|-------------|
| `multimodal/evaluate/` | 4 | Evaluate rows with images through `[ATTACHMENT:...]` placeholders, including rows loaded from a CSV |
| `multimodal/native_metrics/` | 5 | DeepEval image metrics (coherence, helpfulness, image editing, reference, text-to-image) |

---

## All Examples at a Glance

| Category | Count | Frameworks |
|----------|------:|------------|
| Generation | 17 (2 pending) | DeepEval, G-Eval |
| Retrieval | 6 | DeepEval, G-Eval, PyTrec, Custom |
| Tool use | 1 | DeepEval |
| Multimodal | 9 | G-Eval, DeepEval |
| Modify Metrics | 1 | G-Eval |
| Custom Metric | 3 | DeepEval, Custom |
| **Total** | **37 (2 pending)** | |
