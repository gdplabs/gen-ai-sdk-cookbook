@echo off
set UV_INDEX_GEN_AI_INTERNAL_USERNAME=oauth2accesstoken
for /f "delims=" %%i in ('gcloud auth print-access-token') do set UV_INDEX_GEN_AI_INTERNAL_PASSWORD=%%i
uv lock
uv sync
echo Setup completed successfully!
