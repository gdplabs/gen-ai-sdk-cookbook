.PHONY: help sync run-default run-metric run-metric-multiple run-metric-fallback run-evaluator run-evaluator-per-metric run-suite run-yaml run-all

# Default target
.DEFAULT_GOAL := help

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
RED := \033[0;31m
NC := \033[0m # No Color

# UV binary path - try PATH first, then fallback to common locations
UV := $(shell command -v uv 2>/dev/null || echo "$(HOME)/.local/bin/uv")

sync: ## Sync all dependencies from PyPI
	@echo "$(BLUE)📦 Syncing dependencies with UV...$(NC)"
	$(UV) sync && echo "$(GREEN)✓ All dependencies synced successfully!$(NC)"

run-default: ## The default judge, set explicitly on a metric
	@echo "$(BLUE)🚀 Running on the default judge...$(NC)"
	$(UV) run python default_judge.py

run-metric: ## Switch the judge on a metric
	@echo "$(BLUE)🚀 Switching the judge on a metric...$(NC)"
	$(UV) run python metric_judge.py

run-metric-multiple: ## Use multiple judges on a metric
	@echo "$(BLUE)🚀 Running multiple judges on a metric...$(NC)"
	$(UV) run python metric_multiple_judges.py

run-metric-fallback: ## Add a fallback judge to a metric
	@echo "$(BLUE)🚀 Running a metric with a fallback judge...$(NC)"
	$(UV) run python metric_fallback_model.py

run-evaluator: ## Switch the judge on an evaluator
	@echo "$(BLUE)🚀 Switching the judge on an evaluator...$(NC)"
	$(UV) run python evaluator_judge.py

run-evaluator-per-metric: ## Give each metric of an evaluator its own judge
	@echo "$(BLUE)🚀 Running an evaluator with a judge per metric...$(NC)"
	$(UV) run python evaluator_per_metric_models.py

run-suite: ## Switch the judge per suite with evaluate_suites()
	@echo "$(BLUE)🚀 Running suites with their own judges...$(NC)"
	$(UV) run python suite_judges.py

run-yaml: ## Run the YAML suites (set JUDGE_MODEL to switch the judge)
	@echo "$(BLUE)🚀 Running YAML suites...$(NC)"
	$(UV) run python yaml_suites.py

run-all: run-default run-metric run-metric-multiple run-metric-fallback run-evaluator run-evaluator-per-metric run-suite run-yaml ## Run every level

help: ## Show available commands
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(BLUE)%-26s$(NC) %s\n", $$1, $$2}'
