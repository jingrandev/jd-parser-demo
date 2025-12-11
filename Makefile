PYTHON ?= python

.PHONY: test lint format check

test:
	pytest .

lint:
	ruff check .

format:
	ruff format .

check:
	pre-commit run --all-files
