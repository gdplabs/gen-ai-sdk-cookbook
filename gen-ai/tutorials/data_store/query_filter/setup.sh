#!/bin/bash

# Setup script for Unix-based systems
# This script sets up UV authentication and installs dependencies

echo "Setting up UV authentication..."
export UV_INDEX_GEN_AI_INTERNAL_USERNAME=oauth2accesstoken
export UV_INDEX_GEN_AI_INTERNAL_PASSWORD="$(gcloud auth print-access-token)"

echo "Installing dependencies via UV..."
uv lock
uv sync

echo "Setup completed successfully!"
