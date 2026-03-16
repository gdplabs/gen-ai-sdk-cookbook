# Metrics Examples

Runnable examples for evaluating LLM outputs using the `gllm-evals` library. Covers **generation quality**, **retrieval effectiveness**, and **agent behavior** across multiple evaluation frameworks (DeepEval, G-Eval, LangChain, RAGAS, PyTrec).

## Structure

```
metrics/
├── generation/          # Text generation quality metrics (23 examples)
│   └── dataset_examples/
├── retrieval/           # Retrieval/RAG quality metrics (8 examples)
│   └── dataset_examples/
└── agent/               # Agent trajectory and tool-use metrics (2 examples)
    └── dataset_examples/
```

## Prerequisites

- Python >= 3.12
- [uv](https://docs.astral.sh/uv/) package manager
- Access to the internal PyPI index (`gen-ai-internal`)

## Setup

```bash
uv sync
```

Copy `.env.example` to `.env` (or create `.env`) and add your API keys:

```dotenv
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=AIza...
```

## Running Examples

```bash
uv run python generation/example_deepeval_bias.py
uv run python retrieval/example_top_k_accuracy.py
uv run python agent/example_deepeval_tool_correctness.py
```

---

## Generation Metrics

Evaluate the quality of LLM-generated text. Most examples load data from `generation/dataset_examples/` and print a JSON result.

### Data Types

| Type | Fields | Used By |
|------|--------|---------|
| `QAData` | `query`, `generated_response`, `expected_response` | Q&A metrics |
| `RAGData` | `query`, `generated_response`, `retrieved_context`, `expected_retrieved_context` | RAG metrics |
| `SummaryData` | `input`, `summary` | Summarization metrics |

### DeepEval

| Example | Description |
|---------|-------------|
| `example_deepeval_answer_relevancy.py` | Answer is relevant to the query |
| `example_deepeval_bias.py` | Detects bias in responses |
| `example_deepeval_faithfulness.py` | Response stays faithful to retrieved context |
| `example_deepeval_hallucination.py` | Detects hallucinated content |
| `example_deepeval_json_correctness.py` | Validates JSON output against a Pydantic schema |
| `example_deepeval_misuse.py` | Detects misuse potential (domain-aware) |
| `example_deepeval_non_advice.py` | Detects restricted advice types |
| `example_deepeval_pii_leakage.py` | Detects PII in responses |
| `example_deepeval_prompt_alignment.py` | Response aligns with prompt instructions |
| `example_deepeval_role_violation.py` | Detects role specification violations |
| `example_deepeval_toxicity.py` | Detects toxic content |

**Credential required:** `OPENAI_API_KEY`

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

**Credential required:** `GOOGLE_API_KEY`

### LangChain

| Example | Description |
|---------|-------------|
| `example_langchain_conciseness.py` | Response conciseness |
| `example_langchain_correctness.py` | Factual correctness |
| `example_langchain_groundedness.py` | Grounding in context |
| `example_langchain_hallucination.py` | Hallucination detection in RAG |
| `example_langchain_helpfulness.py` | Response helpfulness |

**Credential required:** `OPENAI_API_KEY`

### RAGAS

| Example | Description |
|---------|-------------|
| `example_ragas_factual_correctness.py` | Factual correctness using RAGAS |

**Credential required:** `OPENAI_API_KEY`

### Custom

| Example | Description |
|---------|-------------|
| `example_completeness.py` | Completeness metric |
| `example_groundedness.py` | Groundedness metric |
| `example_language_consistency.py` | Language consistency metric |
| `example_redundancy.py` | Redundancy detection |
| `example_refusal.py` | Refusal evaluation |
| `example_refusal_alignment.py` | Refusal alignment |

---

## Retrieval Metrics

Evaluate the quality of retrieved context in RAG pipelines. Examples load data from `retrieval/dataset_examples/`.

### Data Types

| Type | Fields | Used By |
|------|--------|---------|
| `RAGData` | `query`, `generated_response`, `retrieved_context`, `expected_retrieved_context` | LLM-based retrieval metrics |
| `RetrievalData` | `retrieved_chunks` (dict of chunk_id → score), `ground_truth_chunk_ids` | Ranking metrics |

### Examples

| Example | Framework | Credential | Description |
|---------|-----------|------------|-------------|
| `example_deepeval_contextual_precision.py` | DeepEval | `OPENAI_API_KEY` | Precision of retrieved chunks |
| `example_deepeval_contextual_recall.py` | DeepEval | `OPENAI_API_KEY` | Recall of retrieved chunks |
| `example_deepeval_contextual_relevancy.py` | DeepEval | `OPENAI_API_KEY` | Relevancy of context to query |
| `example_geval_context_sufficiency.py` | G-Eval | `GOOGLE_API_KEY` | Context is sufficient to answer the query |
| `example_ragas_context_precision.py` | RAGAS | `OPENAI_API_KEY` | Context precision (without reference) |
| `example_ragas_context_recall.py` | RAGAS | `OPENAI_API_KEY` | Context recall |
| `example_pytrec_metric.py` | PyTrec | None | NDCG, Precision, Recall at k |
| `example_top_k_accuracy.py` | Custom | None | Top-K hit accuracy |

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

## Agent Metrics

Evaluate agent reasoning trajectories and tool-calling behavior. Examples load data from `agent/dataset_examples/`.

### Data Types

| Type | Fields | Used By |
|------|--------|---------|
| `AgentData` | `query`, `agent_trajectory`, `expected_agent_trajectory` | Trajectory metrics |
| `AgentToolCallData` | `tools_called`, `expected_tools` | Tool-use metrics |

### Examples

| Example | Framework | Credential | Description |
|---------|-----------|------------|-------------|
| `example_langchain_agent_trajectory_accuracy.py` | LangChain | `OPENAI_API_KEY` | Agent follows expected reasoning steps |
| `example_deepeval_tool_correctness.py` | DeepEval | `OPENAI_API_KEY` | Agent calls correct tools with correct arguments |

The tool correctness example also loads a `tool_schema.json` that defines the available tools (e.g., `calculator`, `weather_search`, `send_email`).

---

## All Examples at a Glance

| Category | Count | Frameworks |
|----------|------:|------------|
| Generation | 23 | DeepEval, G-Eval, LangChain, RAGAS, Custom |
| Retrieval | 8 | DeepEval, G-Eval, RAGAS, PyTrec, Custom |
| Agent | 2 | DeepEval, LangChain |
| **Total** | **33** | |
