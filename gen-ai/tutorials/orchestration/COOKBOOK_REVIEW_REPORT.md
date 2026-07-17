# Cookbook Review Report: `gen-ai/tutorials/orchestration/` (PR #94)

Scope: All cookbook files under `gen-ai/tutorials/orchestration/` in the `sync-pipeline` worktree, excluding `.venv`, `__pycache__`, `.ruff_cache`, and lock files.  
Date: 2026-07-18  
Reviewer: Hermes Agent

---

## Executive Summary

| Category | Count |
|---|---|
| Files reviewed | 24 |
| Issues found | 6 |
| reference-only entries | 4 |

All reviewed files contain a docstring URL and a top-level `main` block. The most common convention gaps are: missing `async def main()` in two pipeline examples, absent `load_dotenv()` / hardcoded credential placeholders in routing samples, and lack of explicit `release_resources()` calls.

---

## Issues Found

### 1. `pipeline/input_output_schema_typeddict.py`
- **Line:** 37
- **Problem:** Uses synchronous `def main() -> None:` and calls `asyncio.run(pipe.invoke(...))` instead of `async def main()` with `await pipe.invoke(...)`. This breaks the async-first cookbook convention used by every other orchestration sample.
- **Fix:** Change `def main()` to `async def main()` and wrap the `asyncio.run(...)` block in `if __name__ == "__main__": asyncio.run(main())`.

### 2. `pipeline/pipeline_as_tool.py`
- **Line:** 27
- **Problem:** Uses synchronous `def main() -> None:` while the rest of the cookbook uses `async def main() -> None:`. There is no `await` inside, but consistency with the async-first convention is expected.
- **Fix:** Convert to `async def main() -> None:` or, if the example truly has no async work, add a comment explaining why it is intentionally synchronous.

### 3. `routing/lm-based-router/lm_router.py`
- **Line:** 9–23
- **Problem:** Uses `os.getenv("OPENAI_API_KEY")` to gate execution, but never calls `load_dotenv()` and stores a literal placeholder `"<YOUR_OPENAI_API_KEY>"` in `credentials`. The script is therefore not self-contained: a user must manually export the variable or edit the file.
- **Fix:** Add `from dotenv import load_dotenv` and `load_dotenv()` at the top, and replace the hardcoded placeholder with `os.getenv("OPENAI_API_KEY")` or omit the explicit `credentials=` argument if the SDK reads from the environment automatically.

### 4. `routing/semantic-router/semantic_router_native.py`
- **Line:** 9–23
- **Problem:** Same issue as `lm_router.py`: no `load_dotenv()` and a hardcoded `credentials="<YOUR_OPENAI_API_KEY>"` string. Also identical in structure to `routing/similarity-based-router/semantic_router_native.py`, which suggests copy-paste duplication without adaptation.
- **Fix:** Add `load_dotenv()` and remove the literal placeholder; use environment-based credential loading.

### 5. `routing/similarity-based-router/semantic_router_native.py`
- **Line:** 10–24
- **Problem:** Same missing `load_dotenv()` and hardcoded placeholder pattern. The file header says *"Legacy Similarity-Based Router: deprecated in v0.5"*, but it still ships as a runnable example with the same environment shortcut as the non-legacy file.
- **Fix:** Either remove the file if it is truly deprecated, or update it to load credentials via `load_dotenv()` and align the deprecation notice with actual removal/redirect logic.

### 6. `state/rag_state.py`
- **Line:** 14–28
- **Problem:** Uses synchronous `def main() -> None:` and does not demonstrate a `Pipeline(...)` invocation. It is an introspection script rather than a cookbook example. It also lacks the usual `async def main()` / `await pipe.invoke(...)` pattern, making it inconsistent with the rest of the `state/` section.
- **Fix:** Add a short async pipeline example that creates and invokes a `Pipeline` with `RAGState`, then print the annotated fields as a secondary demonstration. Alternatively, move the introspection script to a `reference/` folder if it is meant to be reference-only.

---

## Reference-Only Status

| File | Correctly marked reference-only? | Rationale |
|---|---|---|
| `composer/reference_only.md` | **Yes** | Composer fluent-builder snippets currently depend on nested `Pipeline().composer...` pieces that are not yet packaged as standalone runnable steps. Publishing fabricated wrappers would mislead users. |
| `steps/reference_only.md` | **Yes** | The GitBook page lists many step types (`if_else`, `switch`, `toggle`, `parallel`, `map_reduce`, `goto`, `while_do`, `try_catch`, `interrupt`, `pause`, etc.) but most fragments are not self-contained. The current stub honestly defers rather than providing broken examples. |
| `pipelines-and-agents/reference_only.md` | **Yes** | The hybrid patterns (`Pipeline-as-a-Tool`, `Agent-as-a-Step`) require `Agent` classes and domain components that cannot be demonstrated in a minimal standalone script. |
| `routing/classifier-router/reference_only.md` | **Yes** | The classifier router requires the optional `gllm-pipeline[llmrouter]` extra, which pulls PyTorch and model artifacts (`.pkl`/`.pt`) that are not installable/verifiable in this worktree. Keeping it reference-only avoids CI/Runtime failures. |

All four reference-only entries include a clear GitBook reference URL and a concise explanation. No further action is needed on these files unless the underlying dependencies are resolved.

---

## Convention Checklist

| Convention | Status |
|---|---|
| Module docstring with GitBook URL | ✅ All 24 reviewed files have a docstring or markdown reference URL. |
| `async def main()` | ⚠️ 2 of 20 Python cookbook files violate this. |
| `release_resources()` | ⚠️ None of the reviewed files call explicit cleanup. Low urgency for short examples, but should be added once longer-lived resources (checkpointer, invoker, router) are used. |
| Self-contained scripts | ⚠️ Routing files depend on manually set `OPENAI_API_KEY` and placeholder text. |
| `load_dotenv()` | ⚠️ Missing in all routing files that read environment variables. |
| ruff compliance | ✅ No obvious style issues in the reviewed files. |
| README completeness | ✅ `pipeline/`, `state/`, `observability_and_debugging/`, and `routing/` all contain `README.md`. |
| Boilerplate files | ✅ Most directories contain `.python-version`, `.env.example`, `setup.sh`, and `setup.bat`. |

---

## Recommendations

1. **Standardize async entrypoints:** Refactor `input_output_schema_typeddict.py` and `pipeline_as_tool.py` to use `async def main()`.
2. **Load env vars consistently:** Add `python-dotenv` boilerplate (`load_dotenv()`) to every routing sample that references `OPENAI_API_KEY` or other secrets.
3. **Remove placeholders:** Replace literal `"<YOUR_OPENAI_API_KEY>"` strings with `os.getenv(...)` lookups.
4. **Decide on `rag_state.py`:** Either turn it into a runnable async example or mark it reference-only and move it out of the primary cookbook flow.
5. **Address deprecation:** Either fix or remove `routing/similarity-based-router/semantic_router_native.py` to avoid shipping duplicate/deprecated code under a different directory name.

---

*No files were modified by this review.*
