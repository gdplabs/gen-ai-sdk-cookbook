.PHONY: run-standard run-directory clean

run-standard:
	uv run python evaluate_suites_from_yaml.py

run-directory:
	uv run python evaluate_suites_from_yaml_dir.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
