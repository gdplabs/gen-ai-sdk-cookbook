.PHONY: help install test run run-all clean lint format check

help:
	@echo "Few-Shot Experiment (Metric-Level) - Makefile Commands"
	@echo ""
	@echo "Available commands:"
	@echo "  make install      - Install dependencies using uv"
	@echo "  make test         - Run quick test with 1 question"
	@echo "  make run          - Run default experiment (experiment 0, all questions)"
	@echo "  make run-all      - Run all experiments (0-14)"
	@echo "  make clean        - Clean output files"
	@echo "  make lint         - Run code quality checks"
	@echo "  make format       - Format code with ruff"
	@echo "  make check        - Run all checks (lint + format)"
	@echo ""

install:
	@echo "Installing dependencies using uv..."
	@echo ""
	@echo "Prerequisites:"
	@echo "  1. uv installed (https://docs.astral.sh/uv/)"
	@echo "  2. gcloud CLI installed and authenticated (gcloud auth login)"
	@echo ""
	@echo "Setting up authentication for private package index..."
	@export UV_INDEX_GEN_AI_INTERNAL_USERNAME=oauth2accesstoken && \
	export UV_INDEX_GEN_AI_INTERNAL_PASSWORD="$$(gcloud auth print-access-token)" && \
	uv sync --all-extras
	@echo ""
	@echo "✅ Dependencies installed from pyproject.toml and uv.lock"
	@echo "Note: Using authenticated access to https://glsdk.gdplabs.id/gen-ai-internal/"

test:
	@echo "Running quick test with 1 question..."
	uv run python experiment_fewshot.py --question-ids 1 --workers 2
	@echo "✅ Test completed"

run:
	@echo "Running default experiment..."
	uv run python experiment_fewshot.py
	@echo "✅ Experiment completed"

run-experiment-%:
	@echo "Running experiment $*..."
	uv run python experiment_fewshot.py --experiment-index $*
	@echo "✅ Experiment $* completed"

run-all:
	@echo "Running all experiments (0-14)..."
	@for i in 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14; do \
		echo ""; \
		echo "========================================"; \
		echo "Running experiment $$i..."; \
		echo "========================================"; \
		uv run python experiment_fewshot.py --experiment-index $$i || exit 1; \
	done
	@echo "✅ All experiments completed"

run-small:
	@echo "Running with small dataset..."
	uv run python experiment_fewshot.py --use-small-data --question-ids 1 2 3
	@echo "✅ Small experiment completed"

clean:
	@echo "Cleaning output files..."
	rm -rf output/
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	rm -rf .ruff_cache/
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	@echo "✅ Cleaned"

lint:
	@echo "Running linters..."
	ruff check .
	@echo "✅ Lint check completed"

format:
	@echo "Formatting code..."
	ruff format .
	@echo "✅ Code formatted"

check: lint format
	@echo "✅ All checks completed"

# Quick runs for specific question sets
run-q1:
	python experiment_fewshot.py --question-ids 1

run-q1-5:
	python experiment_fewshot.py --question-ids 1 2 3 4 5

run-q1-10:
	python experiment_fewshot.py --question-ids 1 2 3 4 5 6 7 8 9 10

# Run with different models
run-gemini:
	python experiment_fewshot.py --eval-model google/gemini-3-flash-preview

run-claude:
	python experiment_fewshot.py --eval-model anthropic/claude-3.5-sonnet

run-gpt4:
	python experiment_fewshot.py --eval-model openai/gpt-4
