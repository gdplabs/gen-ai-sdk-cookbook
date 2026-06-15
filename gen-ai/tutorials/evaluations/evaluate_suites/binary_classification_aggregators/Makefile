.PHONY: install run clean

install:
	uv sync

run:
	uv run python binary_classification_aggregators.py

clean:
	rm -rf .venv
	rm -rf __pycache__
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
