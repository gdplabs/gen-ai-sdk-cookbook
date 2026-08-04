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
- `gcloud` CLI (authenticated) — needed for the internal package registry
- A local clone of `gl-sdk` checked out to the YAML evaluation implementation branch

## Quick Start

```powershell
# 1. Make sure you are on the right SDK branch
cd C:\Users\kalvi\gl-sdk
git checkout f/gllm-evals-evaluate-from-yaml-impl-copy

# 2. Go to this example
cd C:\Users\kalvi\gen-ai-sdk-cookbook\gen-ai\tutorials\evaluations\evaluate_suites\evaluate_suites_from_yaml

# 3. Run the setup script (one-time)
powershell -ExecutionPolicy Bypass -File setup.ps1

# 4. Set up your credentials
cp .env.example .env
# Edit .env and set GOOGLE_API_KEY and OPENAI_API_KEY

# 5. Run the examples
make run-standard
make run-directory
```

## Step-by-Step Installation

### Step 1: Checkout the right SDK branch

```powershell
cd C:\Users\kalvi\gl-sdk
git checkout f/gllm-evals-evaluate-from-yaml-impl-copy
```

### Step 2: Run setup (automatic)

```powershell
cd C:\Users\kalvi\gen-ai-sdk-cookbook\gen-ai\tutorials\evaluations\evaluate_suites\evaluate_suites_from_yaml

powershell -ExecutionPolicy Bypass -File setup.ps1
```

This creates a `.venv`, installs `gllm-evals` and `gllm-inference` from your local
clone (editable, no deps), installs all transitive dependencies from PyPI and the
internal registry, and verifies the install.

To use a different SDK path:

```powershell
powershell -ExecutionPolicy Bypass -File setup.ps1 -GllmSdkPath "D:\other\gl-sdk"
```

### Step 2 (manual): If you prefer to run commands yourself

```powershell
uv venv .venv
uv pip install -p .venv\Scripts\python.exe -e "C:\Users\kalvi\gl-sdk\libs\gllm-evals" --no-deps
uv pip install -p .venv\Scripts\python.exe -e "C:\Users\kalvi\gl-sdk\libs\gllm-inference" --no-deps
uv pip install -p .venv\Scripts\python.exe python-dotenv

# PyPI packages
uv pip install -p .venv\Scripts\python.exe aioboto3 aiohttp cryptography datasets deepmerge filelock filetype google-api-python-client google-auth gspread json-repair jsonschema langfuse orjson pyasn1 pydantic python-box python-magic-bin pytrec-eval-terrier pyyaml sutoppu urllib3 virtualenv deepeval

# Internal packages (requires gcloud auth)
uv pip install -p .venv\Scripts\python.exe --extra-index-url "https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/" gllm-core
```

### Step 3: Set up credentials

```powershell
cp .env.example .env
# Edit .env and set GOOGLE_API_KEY and OPENAI_API_KEY
```

### Step 4: Verify

```powershell
make verify
# or directly:
.venv\Scripts\python.exe -c "from gllm_evals import EvalSuite; print('from_yaml:', hasattr(EvalSuite, 'from_yaml'))"
```

Expected output: `from_yaml: True`

## Usage

```powershell
make run-standard   # evaluate_suites_from_yaml.py
make run-directory  # evaluate_suites_from_yaml_dir.py
```

Or directly:

```powershell
.venv\Scripts\python.exe evaluate_suites_from_yaml.py
.venv\Scripts\python.exe evaluate_suites_from_yaml_dir.py
```

## When YAML features are released

Once `gllm-evals` ships with YAML support to the internal registry, revert
`pyproject.toml` to use registry sources:

```toml
[[tool.uv.index]]
name = "gen-ai-internal"
url = "https://glsdk.gdplabs.id/gen-ai-internal/simple/"

[tool.uv.sources]
gllm-evals = { index = "gen-ai-internal" }
gllm-inference = { index = "gen-ai-internal" }

[project]
dependencies = [
    "gllm-evals[deepeval]>=0.1.23,<0.2.0",
    "gllm-inference>=0.6.64,<0.7.0",
    "python-dotenv>=1.0.0,<2.0.0",
]
```

Then `uv sync` will work normally.
