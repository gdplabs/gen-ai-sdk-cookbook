PACKAGE    := $(shell basename $(CURDIR))

.PHONY: install run run-query run-question test test-query test-question

install:
	export UV_INDEX_GEN_AI_INTERNAL_USERNAME=oauth2accesstoken && \
	export UV_INDEX_GEN_AI_INTERNAL_PASSWORD="$$(gcloud auth print-access-token)" && \
	uv sync --all-extras

run:
	python -m $(PACKAGE).runner

run-query:
	python -m $(PACKAGE).runner --query-id $(IDS)

run-question:
	python -m $(PACKAGE).runner --question-id $(IDS)

test:
	pytest

test-query:
	pytest --query-id $(IDS)

test-question:
	pytest --question-id $(IDS)
