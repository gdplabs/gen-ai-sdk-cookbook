<#
.SYNOPSIS
    One-time setup for the YAML evaluation cookbook.
.DESCRIPTION
    Creates a venv, installs gllm-evals and gllm-inference from local paths,
    then installs all transitive dependencies from PyPI and the internal registry.
.PARAMETER GllmSdkPath
    Path to the gl-sdk repo root. Defaults to C:\Users\kalvi\gl-sdk.
.EXAMPLE
    .\setup.ps1
    .\setup.ps1 -GllmSdkPath "D:\other\gl-sdk"
#>
param(
    [string]$GllmSdkPath = "C:\Users\kalvi\gl-sdk"
)

$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition

Write-Host "==> Creating venv..." -ForegroundColor Cyan
uv venv "$scriptDir\.venv"
$pip = "$scriptDir\.venv\Scripts\python.exe"

Write-Host "==> Installing gllm-evals and gllm-inference from local paths..." -ForegroundColor Cyan
uv pip install -p $pip -e "$GllmSdkPath\libs\gllm-evals" --no-deps
uv pip install -p $pip -e "$GllmSdkPath\libs\gllm-inference" --no-deps
uv pip install -p $pip python-dotenv

Write-Host "==> Installing PyPI dependencies..." -ForegroundColor Cyan
uv pip install -p $pip `
    aioboto3 aiohttp cryptography datasets deepmerge filelock filetype `
    google-api-python-client google-auth gspread json-repair jsonschema `
    langfuse orjson pyasn1 pydantic python-box python-magic-bin `
    pytrec-eval-terrier pyyaml sutoppu urllib3 virtualenv deepeval

Write-Host "==> Installing gllm-core from internal registry..." -ForegroundColor Cyan
$token = gcloud auth print-access-token
uv pip install -p $pip `
    --extra-index-url "https://oauth2accesstoken:$token@glsdk.gdplabs.id/gen-ai-internal/simple/" `
    gllm-core

Write-Host "`n==> Verifying..." -ForegroundColor Cyan
& $pip -c "from gllm_evals import EvalSuite; print('from_yaml:', hasattr(EvalSuite, 'from_yaml'))"

Write-Host "`nDone! Run the examples with:" -ForegroundColor Green
Write-Host "  .venv\Scripts\python.exe evaluate_suites_from_yaml.py"
Write-Host "  .venv\Scripts\python.exe evaluate_suites_from_yaml_dir.py"
