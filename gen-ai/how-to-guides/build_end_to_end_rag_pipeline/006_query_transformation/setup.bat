@echo off

REM Setup script for Windows systems
REM This script sets up UV authentication and installs dependencies

echo Setting up UV authentication...
set UV_INDEX_GEN_AI_INTERNAL_USERNAME=oauth2accesstoken
for /f "delims=" %%i in ('gcloud auth print-access-token') do set UV_INDEX_GEN_AI_INTERNAL_PASSWORD=%%i

echo Installing dependencies via UV...
uv lock
uv sync

echo Setup completed successfully!
