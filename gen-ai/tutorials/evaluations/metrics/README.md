# Metrics Examples

Examples for LLM output evaluation with `gllm-evals-binary`. These cover generation quality, retrieval, prompt alignment, tool use, and multimodal inputs.

## Structure

```
metrics/
├── generation/          # Text generation quality metrics (18 examples)
│   └── dataset_examples/
├── retrieval/           # Retrieval/RAG quality metrics (8 examples)
│   └── dataset_examples/
├── tool_use/            # Tool-use metrics (1 example)
│   └── dataset_examples/
├── multimodal/          # Image-aware evaluation (9 examples)
├── conversational/      # Multi-turn conversation metrics (12 examples)
├── modify_metrics/      # How to modify existing metric attributes (1 example, own project)
└── custom_metric/       # How to create custom metrics (3 approaches, own project)
```

## Prerequisites

- Python >= 3.12
- [uv](https://docs.astral.sh/uv/) package manager

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
uv run python conversational/example_turn_aggregation.py
```

### Data

The JSONL files in each `dataset_examples/` folder hold one test case per line and use `LLMTestCase` field names (`input`, `actual_output`, `expected_output`, `retrieved_context`, `expected_context`). `DictDataset.from_jsonl(...).load()` returns `LLMTestCase` rows, so an example reads a row with attribute access, for example `data[0].input`. These datasets are flat, so they can also be loaded from CSV with `DictDataset.from_csv(...)`.

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
| `example_geval_conciseness.py` | Response conciseness |
| `example_geval_groundedness.py` | Factual grounding in retrieved context |
| `example_geval_helpfulness.py` | Response helpfulness |
| `example_geval_language_consistency.py` | Language consistency |
| `example_geval_redundancy.py` | Detects redundant/repetitive content |
| `example_geval_refusal.py` | Evaluates proper refusal behavior |
| `example_geval_refusal_alignment.py` | Refusal alignment with expected behavior |
| `example_geval_summarization_coherence.py` | Summary coherence |
| `example_geval_summarization_consistency.py` | Summary factual consistency |
| `example_geval_summarization_fluency.py` | Summary fluency |
| `example_geval_summarization_relevance.py` | Summary relevance |

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

The example loads `LLMTestCase` rows with `tools_called` and `expected_tools` from `tool_use/dataset_examples/simple_agent_tool_call_data.jsonl`, and a `tool_schema.json` that defines the available tools (e.g., `calculator`, `weather_search`, `send_email`).

---

## Multimodal

| Folder | Examples | Description |
|--------|---------:|-------------|
| `multimodal/evaluate/` | 4 | Evaluate rows with images through `[ATTACHMENT:...]` placeholders, including rows loaded from a CSV |
| `multimodal/native_metrics/` | 5 | DeepEval image metrics (coherence, helpfulness, image editing, reference, text-to-image) |

---

## Conversational Metrics

Evaluate a whole multi-turn conversation rather than a single row. Each example scores a good and a bad conversation with the same metric.

### Data Type

| Type | Fields | Notes |
|------|--------|-------|
| `ConversationalTestCase` | `turns`, `chatbot_role`, `expected_output`, `scenario` | `turns` is a list of `Turn(role, content, retrieved_context, tools_called)` |

### Examples

| Example | Metric | Demonstrates |
|---------|--------|--------------|
| `example_knowledge_retention.py` | `DeepEvalKnowledgeRetentionMetric` | forgets an order number vs recalls it |
| `example_conversation_completeness.py` | `DeepEvalConversationCompletenessMetric` | two user intents ignored vs both satisfied |
| `example_goal_accuracy.py` | `DeepEvalGoalAccuracyMetric` | booking completed vs abandoned |
| `example_topic_adherence.py` | `DeepEvalTopicAdherenceMetric` | off-topic question declined vs answered |
| `example_conversational_geval.py` | `DeepEvalConversationalGEvalMetric` | a custom criterion |
| `example_turn_aggregation.py` | `DeepEvalTurnFaithfulnessMetric` | `MEAN` vs `WORST_TURN` vs a custom aggregator |
| `example_turn_relevancy.py` | `DeepEvalTurnRelevancyMetric` | off-topic reply vs on-topic reply |
| `example_turn_contextual_precision.py` | `DeepEvalTurnContextualPrecisionMetric` | relevant document ranked last vs first |
| `example_turn_contextual_recall.py` | `DeepEvalTurnContextualRecallMetric` | retrieval misses the answer vs covers it |
| `example_turn_contextual_relevancy.py` | `DeepEvalTurnContextualRelevancyMetric` | unrelated retrieval vs relevant retrieval |
| `example_role_adherence.py` | `DeepEvalRoleAdherenceMetric` | assistant turns rude vs stays in role |
| `example_tool_use.py` | `DeepEvalToolUseMetric` | wrong tool called vs right tool called |

**Credential required:** `OPENROUTER_API_KEY` for the SDK default judge, `openrouter/deepseek/deepseek-v4.1-flash-1017`. Copy `.env.example` to `.env` and set it there. These examples pass no explicit `models=`. A judge call can time out (`GLLM-EVAL-TIMEOUT`); rerun the example.

The last seven score a conversation turn by turn, and each has a single-turn twin for `LLMTestCase` rows: `DeepEvalFaithfulnessMetric`, `DeepEvalAnswerRelevancyMetric`, `DeepEvalContextualPrecisionMetric`, `DeepEvalContextualRecallMetric`, `DeepEvalContextualRelevancyMetric`, `DeepEvalRoleViolationMetric` and `DeepEvalToolCorrectnessMetric`.

See [Multi-turn Evaluation](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation/multiturn-evaluation) for turn aggregation and the `BaseTurnAggregator` contract.

---

## All Examples at a Glance

| Category | Count | Frameworks |
|----------|------:|------------|
| Generation | 17 | DeepEval, G-Eval |
| Retrieval | 6 | DeepEval, G-Eval, PyTrec, Custom |
| Tool use | 1 | DeepEval |
| Multimodal | 9 | G-Eval, DeepEval |
| Conversational | 12 | DeepEval |
| Modify Metrics | 1 | G-Eval |
| Custom Metric | 3 | DeepEval, Custom |
| **Total** | **49** | |
