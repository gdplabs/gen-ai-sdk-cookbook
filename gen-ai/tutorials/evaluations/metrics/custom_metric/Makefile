.PHONY: help install run clean

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies using uv
	export UV_INDEX_GEN_AI_INTERNAL_USERNAME=oauth2accesstoken && \
	export UV_INDEX_GEN_AI_INTERNAL_PASSWORD="$$(gcloud auth print-access-token)" && \
	uv venv .venv && \
	. .venv/bin/activate && \
	uv lock && \
	uv sync

run-approach1: ## Run Approach 1: DeepEvalGEvalMetric directly
	uv run python approach1_deepeval_geval_direct.py

run-approach2: ## Run Approach 2: Subclass DeepEvalGEvalMetric
	uv run python approach2_test_politeness.py

run-approach3: ## Run Approach 3: Subclass BaseMetric
	uv run python approach3_test_order_exists.py

clean: ## Clean up generated files
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.log" -delete
	rm -rf .pytest_cache
