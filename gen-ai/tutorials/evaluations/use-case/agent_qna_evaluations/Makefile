.PHONY: help sync setup-auth install clean run-eval run-eval-calibrated pre-commit

# Default target
.DEFAULT_GOAL := help

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

# UV binary path - try PATH first, then fallback to common locations
UV := $(shell command -v uv 2>/dev/null || echo "$(HOME)/.local/bin/uv")

# Private registries
REGISTRY_INTERNAL := https://us-central1-python.pkg.dev/gen-ai-internal-421607/gen-ai-internal/simple
REGISTRY_GEN_AI := https://us-central1-python.pkg.dev/gen-ai-internal-421607/gen-ai/simple

sync: ## Sync all dependencies including private packages
	@echo "$(BLUE)🔐 Getting Google Cloud access token...$(NC)"
	@TOKEN=$$(gcloud auth print-access-token 2>/dev/null); \
	if [ -z "$$TOKEN" ]; then \
		echo "$(RED)✗ Failed to get gcloud token$(NC)"; \
		echo "  Run: gcloud auth login"; \
		exit 1; \
	fi; \
	echo "$(GREEN)✓ Got access token$(NC)"; \
	echo ""; \
	echo "$(BLUE)📦 Syncing dependencies with UV...$(NC)"; \
	export UV_PYTHON=python3.12; \
	export UV_INDEX_GEN_AI_USERNAME=oauth2accesstoken; \
	export UV_INDEX_GEN_AI_PASSWORD="$$TOKEN"; \
	export UV_INDEX_GEN_AI_INTERNAL_USERNAME=oauth2accesstoken; \
	export UV_INDEX_GEN_AI_INTERNAL_PASSWORD="$$TOKEN"; \
	$(UV) sync && echo "$(GREEN)✓ All dependencies synced successfully!$(NC)"

run-eval: ## Run the CSV-based multi-case agent evaluation
	@echo "$(BLUE)🚀 Running Agent QnA Evaluation (CSV dataset)...$(NC)"
	$(UV) run python eval.py

run-eval-calibrated: ## Run the calibrated evaluation with context sufficiency metric
	@echo "$(BLUE)🚀 Running Calibrated Agent QnA Evaluation...$(NC)"
	$(UV) run python eval_calibrated.py

help: ## Show available commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(BLUE)%-24s$(NC) %s\n", $$1, $$2}'

.PHONY: help setup-auth sync install clean run-eval run-eval-calibrated pre-commit
