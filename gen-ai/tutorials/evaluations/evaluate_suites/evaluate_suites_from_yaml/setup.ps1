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

Write-Host "==> Installing all transitive dependencies..." -ForegroundColor Cyan
uv pip install -p $pip `
    aioboto3 aiofiles aiohttp av cryptography datasets deepmerge `
    filetype httpx jinja2 jsonref json-repair jsonschema `
    langchain "langfuse>=3.2.1,<4.0.0" numpy orjson pandas prompt-toolkit protobuf `
    pyasn1 pydantic python-box python-magic-bin python-dotenv `
    pytrec-eval-terrier pyyaml sentencepiece sutoppu urllib3 virtualenv "deepeval>=3.7.0,<4.0.0" `
    google-genai "openai[aiohttp]"

Write-Host "==> Installing gllm-core from internal registry..." -ForegroundColor Cyan
$token = gcloud auth print-access-token
uv pip install -p $pip `
    --extra-index-url "https://oauth2accesstoken:$token@glsdk.gdplabs.id/gen-ai-internal/simple/" `
    gllm-core

Write-Host "`n==> Verifying..." -ForegroundColor Cyan
& $pip -c "from gllm_evals import EvalSuite; print('from_yaml:', hasattr(EvalSuite, 'from_yaml'))"

Write-Host "`nDone! Run the examples with:" -ForegroundColor Green
Write-Host "  make run-standard"
Write-Host "  make run-directory"
