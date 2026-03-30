PACKAGE    := $(shell basename $(CURDIR))

.PHONY: install test test-verbose test-collect test-keyword

install:
	export UV_INDEX_GEN_AI_INTERNAL_USERNAME=oauth2accesstoken && \
	export UV_INDEX_GEN_AI_INTERNAL_PASSWORD="$$(gcloud auth print-access-token)" && \
	uv sync --all-extras

test:
	pytest evaluations/

test-verbose:
	pytest evaluations/ -v

test-collect:
	pytest evaluations/ --collect-only

test-keyword:
	@if [ -z "$(KEYWORD)" ]; then \
		echo "Usage: make test-keyword KEYWORD='no_48 or no_64'"; \
		exit 1; \
	fi
	pytest evaluations/ -k "$(KEYWORD)" -v
