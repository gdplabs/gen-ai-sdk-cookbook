@echo off

REM Setup script for Windows systems
REM This script sets up UV authentication and installs dependencies

where gcloud >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: gcloud CLI is not installed.
    echo Install from: https://cloud.google.com/sdk/docs/install
    exit /b 1
)

gcloud auth print-access-token >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: Not authenticated with gcloud.
    echo Run: gcloud auth login
    exit /b 1
)

echo Setting up UV authentication...
set UV_INDEX_GEN_AI_INTERNAL_USERNAME=oauth2accesstoken
for /f "delims=" %%i in ('gcloud auth print-access-token') do set UV_INDEX_GEN_AI_INTERNAL_PASSWORD=%%i

echo Installing dependencies via UV...
uv lock
uv sync

echo Setup completed successfully!
