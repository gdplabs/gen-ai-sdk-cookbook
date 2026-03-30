PACKAGE    := $(shell basename $(CURDIR))

.PHONY: install test test-query test-question

install:
	export UV_INDEX_GEN_AI_INTERNAL_USERNAME=oauth2accesstoken && \
	export UV_INDEX_GEN_AI_INTERNAL_PASSWORD="$$(gcloud auth print-access-token)" && \
	uv sync --all-extras

test:
	pytest

test-query:
	pytest --query-id $(IDS)

test-question:
	pytest --question-id $(IDS)
