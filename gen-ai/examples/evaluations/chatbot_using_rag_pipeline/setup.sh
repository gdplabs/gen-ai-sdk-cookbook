#!/bin/bash

# Setup script for Unix-based systems
# This script sets up UV authentication and installs dependencies

if ! command -v gcloud &> /dev/null; then
    echo "Error: gcloud CLI is not installed."
    echo "Install from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

if ! gcloud auth print-access-token &> /dev/null; then
    echo "Error: Not authenticated with gcloud."
    echo "Run: gcloud auth login"
    exit 1
fi

echo "Setting up UV authentication..."
export UV_INDEX_GEN_AI_INTERNAL_USERNAME=oauth2accesstoken
export UV_INDEX_GEN_AI_INTERNAL_PASSWORD="$(gcloud auth print-access-token)"

echo "Installing dependencies via UV..."
uv lock
uv sync

echo "Setup completed successfully!"
