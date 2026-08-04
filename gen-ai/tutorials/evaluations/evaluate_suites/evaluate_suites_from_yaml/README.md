# Evaluate Suites from YAML

This example covers the two YAML evaluation flows:

| Flow | Entry point | Demonstrates |
|---|---|---|
| Standard YAML | `evaluate_suites_from_yaml.py` | One YAML file with `ExactMatchMetric` via `class_path`, `KeywordMatchMetric` via registry, model credentials, and a fallback model |
| YAML directory | `evaluate_suites_from_yaml_dir.py` | All SDK sample suites loaded together, including `CompositeEvaluator` |

The standard flow reads only `sample_suites/custom_judge_model_and_metrics_suite.yaml`. The directory flow reads every YAML file under `sample_suites/`.

## Prerequisites

- Python 3.11 or higher
- `uv`
- A local clone of `gl-sdk` at `C:/Users/kalvi/gl-sdk` checked out to the branch with the YAML evaluation implementation
- API keys for the LLM-based suites (set in `.env` after the steps below)

## Installation

### Step 1: Install SDK packages into the cookbook venv

`uv sync` cannot resolve this cookbook yet because the local `gllm-evals` 0.0.0 package depends on `gllm-inference[anthropic]>=0.6.64,<0.7.0`, which conflicts with the local `gllm-inference` 0.0.0. Install both packages directly via editable path, with `--no-deps` to skip the conflicting metadata-driven resolution:

```bash
cd "C:/Users/kalvi/gen-ai-sdk-cookbook/gen-ai/tutorials/evaluations/evaluate_suites/evaluate_suites_from_yaml"

uv venv .venv
uv pip install -p .venv/Scripts/python.exe -e "C:/Users/kalvi/gl-sdk/libs/gllm-evals" --no-deps
uv pip install -p .venv/Scripts/python.exe -e "C:/Users/kalvi/gl-sdk/libs/gllm-inference" --no-deps
uv pip install -p .venv/Scripts/python.exe python-dotenv
```

### Step 2: Install runtime dependencies

`--no-deps` skipped all transitive dependencies. Install them now using the internal registry:

```bash
gcloud auth print-access-token  # copy this token

uv pip install -p .venv/Scripts/python.exe \
  --index-url "https://oauth2accesstoken:<PASTE-TOKEN>@glsdk.gdplabs.id/gen-ai-internal/simple/" \
  aioboto3 aiohttp cryptography datasets deepmerge filelock filetype \
  google-api-python-client google-auth gspread json-repair jsonschema \
  langfuse orjson pyasn1 pydantic python-box python-magic-bin \
  pytrec-eval-terrier pyyaml sutoppu urllib3 virtualenv deepeval gllm-core
```

### Step 3: Set up credentials

```bash
cp .env.example .env
# Edit .env and set GOOGLE_API_KEY and OPENAI_API_KEY
```

### Step 4: Verify the install

```bash
.venv/Scripts/python.exe -c "from gllm_evals import EvalSuite; print('from_yaml:', hasattr(EvalSuite, 'from_yaml'))"
```

If `from_yaml` prints `True`, the install is correct.

## Usage

```bash
.venv/Scripts/python.exe evaluate_suites_from_yaml.py
.venv/Scripts/python.exe evaluate_suites_from_yaml_dir.py
```

Or via `make`:

```bash
make run-standard
make run-directory
```

## When YAML features are released

Once `gllm-evals` `>= 0.1.23` ships with YAML support, replace the path-based install with registry resolution. Update `pyproject.toml`:

```toml
[[tool.uv.index]]
name = "gen-ai-internal"
url = "https://glsdk.gdplabs.id/gen-ai-internal/simple/"

[tool.uv.sources]
gllm-evals = { index = "gen-ai-internal" }

[project]
dependencies = [
    "gllm-evals[deepeval]>=0.1.23,<0.2.0",
    "gllm-inference>=0.6.64,<0.7.0",
    "python-dotenv>=1.0.0,<2.0.0",
]
```

Then run `uv sync` normally.
