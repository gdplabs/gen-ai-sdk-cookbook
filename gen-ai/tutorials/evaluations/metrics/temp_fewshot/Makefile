.PHONY: help install run clean

help:
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:
	export UV_INDEX_GEN_AI_INTERNAL_USERNAME=oauth2accesstoken && \
	export UV_INDEX_GEN_AI_INTERNAL_PASSWORD="$$(gcloud auth print-access-token)" && \
	uv venv .venv && \
	. .venv/bin/activate && \
	uv lock && \
	uv sync

run:
	uv run python example_temp_fewshot.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.log" -delete
	rm -rf .pytest_cache
