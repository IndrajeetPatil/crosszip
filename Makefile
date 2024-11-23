.EXPORT_ALL_VARIABLES:
SHELL=/bin/bash
VIRTUAL_ENV ?= ${PWD}/.venv

venv:
	rm -rf $(VIRTUAL_ENV) && python3.13 -m venv $(VIRTUAL_ENV)
	$(VIRTUAL_ENV)/bin/pip install --upgrade pip
	pip install uv
	uv sync --frozen

activate:
	. $(VIRTUAL_ENV)/bin/activate

## Test package

test: activate
	$(VIRTUAL_ENV)/bin/pytest . -vv --random-order

coverage: activate
	$(VIRTUAL_ENV)/bin/coverage run -m pytest . && $(VIRTUAL_ENV)/bin/coverage report --fail-under=95 && $(VIRTUAL_ENV)/bin/coverage html;

test-package: test coverage

## Code quality

format:
	$(VIRTUAL_ENV)/bin/pre-commit run --hook-stage commit ruff-format --all-files

lint:
	$(VIRTUAL_ENV)/bin/pre-commit run --hook-stage commit ruff --all-files

mypy:
	$(VIRTUAL_ENV)/bin/pre-commit run --hook-stage commit mypy --all-files

qa: format lint mypy

## Check package

build: activate
	uv build

check-package: test-package qa build


help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  venv           Create a virtual environment"
	@echo "  activate       Activate the virtual environment"
	@echo "  test           Run tests"
	@echo "  coverage       Run tests and generate coverage report"
	@echo "  test-package   Run tests, generate coverage report and check coverage"
	@echo "  format         Format code"
	@echo "  lint           Lint code"
	@echo "  mypy           Type check code"
	@echo "  qa             Run format, lint and mypy"
	@echo "  build          Build package"
	@echo "  check-package  Run tests, generate coverage report, check coverage, format, lint, mypy and build"
	@echo "  help           Show this help message"
	@echo ""
	@echo "Variables:"
	@echo "  VIRTUAL_ENV    Path to the virtual environment"
	@echo ""
	@echo "Examples:"
	@echo "  make test"
	@echo "  make coverage"
	@echo "  make test-package"
	@echo "  make format"
	@echo "  make lint"
	@echo "  make mypy"
	@echo "  make qa"
	@echo "  make build"
	@echo "  make check-package"
	@echo "  make help"
	@echo ""
	@echo "For more information, see the Makefile"
	@echo ""