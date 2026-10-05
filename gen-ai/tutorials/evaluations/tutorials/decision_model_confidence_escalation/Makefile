.PHONY: help install run run-quickstart run-escalation clean

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

run: run-quickstart run-escalation ## Run both examples

run-quickstart: ## Read a decision model judge's decision
	uv run python read_judge_decision.py

run-escalation: ## Escalate a low-confidence result to a stronger model
	uv run python escalate_to_stronger_model.py

clean: ## Clean up generated files
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.log" -delete
	rm -rf .pytest_cache
	rm -rf gllm_evals
	rm -rf .deepeval
