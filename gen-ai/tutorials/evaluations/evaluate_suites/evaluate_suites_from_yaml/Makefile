.PHONY: run-standard run-directory clean

run-standard:
	.venv/Scripts/python.exe evaluate_suites_from_yaml.py

run-directory:
	.venv/Scripts/python.exe evaluate_suites_from_yaml_dir.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name "gllm_evals" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".deepeval" -exec rm -rf {} + 2>/dev/null || true
