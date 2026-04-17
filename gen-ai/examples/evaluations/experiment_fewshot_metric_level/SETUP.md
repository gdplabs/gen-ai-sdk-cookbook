# Quick Setup Guide for Developers

This experiment is **fully standalone** and can be run independently without the parent SDK repository.

## Prerequisites

1. **Python 3.11-3.13** installed
2. **gcloud CLI** ([install here](https://cloud.google.com/sdk/docs/install))
3. **gcloud authentication** - must be logged in with `gcloud auth login`
4. **Network access** to GDPLabs internal package index: `https://glsdk.gdplabs.id/gen-ai-internal/`
5. **API Key** for your chosen LLM provider (Google, Anthropic, OpenAI)

## Installation Steps

```bash
# 1. Authenticate with gcloud (if not already done)
gcloud auth login

# 2. Navigate to the experiment directory
cd experiment_fewshot_metric_level

# 3. Install dependencies with authenticated access
make install

# OR manually:
pip install --extra-index-url "https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-evals[deepeval,langchain,ragas]" pandas python-dotenv

# 4. Configure API key
cp .env.example .env
# Edit .env and add your API key
```

## Quick Test

```bash
# Run a quick test with 1 question
make test

# Expected output: Successful evaluation of 1 row
```

## Run Full Experiment

```bash
# Run specific experiment (e.g., botanica)
python experiment_fewshot.py \
  --experiment-index botanica \
  --eval-model google/gemini-3-flash-preview \
  --workers 5 \
  --question-ids 1 2 3 4 5
```

## Key Points for Standalone Setup

✅ **No parent repository needed** - `gllm-evals` is installed from package index via pip
✅ **Self-contained** - All data files included in this directory
✅ **Portable** - Can be copied/cloned anywhere
✅ **No path dependencies** - Uses authenticated package index, not local file paths
✅ **GCP Authentication** - Uses gcloud credentials for secure package access

## Troubleshooting

### Can't access package index?
```bash
# 1. Check if you're logged in to gcloud
gcloud auth list

# 2. Login if needed
gcloud auth login

# 3. Verify access token works
gcloud auth print-access-token

# 4. Test package index access
curl -I https://glsdk.gdplabs.id/gen-ai-internal/simple/
```
If this fails, check VPN/firewall settings or contact DevOps.

### Dependencies fail to install?
```bash
# 1. Ensure gcloud is authenticated
gcloud auth login

# 2. Reinstall
pip install --extra-index-url "https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-evals[deepeval,langchain,ragas]" pandas python-dotenv

# 3. If still failing, check your GCP permissions
gcloud auth application-default login
```

### API key not working?
```bash
# Check environment variable
echo $GOOGLE_API_KEY

# Or check .env file
cat .env
```

## What's Different from Monorepo Setup?

| Aspect | Monorepo Setup | Standalone Setup |
|--------|---------------|------------------|
| Dependency | Local path `..` | Authenticated package index |
| Authentication | None | gcloud auth required |
| Installation | `cd .. && uv sync` | `pip install` with gcloud token |
| Execution | `../.venv/bin/python` | `python` (system/venv) |
| Portability | Requires parent SDK | Fully portable (with gcloud) |

## Files Included

```
experiment_fewshot_metric_level/
├── pyproject.toml          # Standalone dependencies
├── experiment_fewshot.py   # Main script
├── evaluator.py           # Evaluation logic
├── config.py              # Experiment configs
├── utils.py               # Helper functions
├── Makefile               # Convenience commands
├── README.md              # Full documentation
├── .env.example           # API key template
└── data/
    ├── botanica_experiment.csv    # Experiment data
    └── fewshot_examples.json      # Few-shot examples (3.2MB)
```

## Contact

For issues or questions, contact the SDK team or check the main README.md for detailed documentation.
