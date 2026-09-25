.PHONY: help sync run-step0 run-step1 run-step2 run-step3 run-step4 run-all

# Default target
.DEFAULT_GOAL := help

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
RED := \033[0;31m
NC := \033[0m # No Color

# UV binary path - try PATH first, then fallback to common locations
UV := $(shell command -v uv 2>/dev/null || echo "$(HOME)/.local/bin/uv")

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
	export UV_INDEX_GEN_AI_INTERNAL_USERNAME=oauth2accesstoken; \
	export UV_INDEX_GEN_AI_INTERNAL_PASSWORD="$$TOKEN"; \
	$(UV) sync && echo "$(GREEN)✓ All dependencies synced successfully!$(NC)"

run-step0: ## Step 0: Run a metric on the default judge (needs GOOGLE_API_KEY)
	@echo "$(BLUE)🚀 Step 0: Running on the default judge...$(NC)"
	$(UV) run python step0_default_judge.py

run-step1: ## Step 1: Switch the judge on a metric
	@echo "$(BLUE)🚀 Step 1: Switching the metric judge...$(NC)"
	$(UV) run python step1_metric_judge.py

run-step2: ## Step 2: Switch the judge on an evaluator
	@echo "$(BLUE)🚀 Step 2: Switching the evaluator judge...$(NC)"
	$(UV) run python step2_evaluator_judge.py

run-step3: ## Step 3: Switch the judge per suite with evaluate_suites()
	@echo "$(BLUE)🚀 Step 3: Running suites with different judges...$(NC)"
	$(UV) run python step3_suite_judges.py

run-step4: ## Step 4: Run the YAML suites (set JUDGE_MODEL to switch the judge)
	@echo "$(BLUE)🚀 Step 4: Running YAML suites...$(NC)"
	$(UV) run python step4_yaml_suites.py

run-all: run-step0 run-step1 run-step2 run-step3 run-step4 ## Run every step

help: ## Show available commands
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(BLUE)%-24s$(NC) %s\n", $$1, $$2}'
