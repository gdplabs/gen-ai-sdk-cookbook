.PHONY: install run-standard run-directory clean verify

SDK_PATH ?= C:/Users/kalvi/gl-sdk

install:
	powershell -ExecutionPolicy Bypass -File setup.ps1 -GllmSdkPath "$(SDK_PATH)"

verify:
	.venv/Scripts/python.exe -c "from gllm_evals import EvalSuite; print('from_yaml:', hasattr(EvalSuite, 'from_yaml'))"

run-standard:
	.venv/Scripts/python.exe evaluate_suites_from_yaml.py

run-directory:
	.venv/Scripts/python.exe evaluate_suites_from_yaml_dir.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf gllm_evals/ .deepeval/ 2>/dev/null || true
