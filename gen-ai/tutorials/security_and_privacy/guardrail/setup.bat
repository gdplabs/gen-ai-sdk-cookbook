@echo off
echo Setting up UV authentication...
for /f "tokens=*" %%a in ('gcloud auth print-access-token') do set UV_INDEX_GEN_AI_INTERNAL_PASSWORD=%%a
set UV_INDEX_GEN_AI_INTERNAL_USERNAME=oauth2accesstoken

echo Installing dependencies via UV...
uv lock
uv sync

echo Setup completed successfully!
