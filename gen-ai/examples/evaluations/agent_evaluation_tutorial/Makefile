.PHONY: help install run run-available-tools run-trajectory run-evaluate-helper clean

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

run: ## Run basic agent evaluation
	uv run python main.py

run-available-tools: ## Run agent evaluation with available tools context
	uv run python main_with_available_tools.py

run-trajectory: ## Run agent evaluation with trajectory accuracy
	uv run python main_with_trajectory.py

run-evaluate-helper: ## Run agent evaluation with evaluate helper function
	uv run python main_with_evaluate_helper.py

clean: ## Clean up generated files
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.log" -delete
	rm -rf .pytest_cache
