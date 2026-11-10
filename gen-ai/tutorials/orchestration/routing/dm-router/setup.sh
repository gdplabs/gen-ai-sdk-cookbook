#!/bin/bash
set -euo pipefail
export UV_INDEX_GEN_AI_INTERNAL_USERNAME=oauth2accesstoken
export UV_INDEX_GEN_AI_INTERNAL_PASSWORD="$(gcloud auth print-access-token)"
uv lock
uv sync
echo "Setup completed!"
