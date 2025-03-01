## Dependencies
update-deps:
	uv lock --upgrade
	uv sync

upgrade-deps: update-deps

## Code quality

format:
	uv run ruff format

lint:
	uv run ruff check --fix

mypy:
	uv run mypy .

qa: format lint mypy

## Check package

test: 
	uv run pytest .

coverage: 
	uv run coverage run -m pytest . 
	uv run coverage report
	uv run coverage html

build:
	uv build

test-package: test coverage
check-package: test-package qa build

## Docs

serve-docs:
	uv run quarto render README.qmd
	cp README.md docs/index.md
	cp CHANGELOG.md docs/changelog.md
	uv run mkdocs build 
	uv run mkdocs serve

help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  update-deps    Update dependencies"
	@echo "  test           Run tests"
	@echo "  coverage       Run tests and generate coverage report"
	@echo "  test-package   Run tests, generate coverage report and check coverage"
	@echo "  format         Format code"
	@echo "  lint           Lint code"
	@echo "  mypy           Type check code"
	@echo "  qa             Run format, lint and mypy"
	@echo "  build          Build package"
	@echo "  check-package  Run tests, generate coverage report, check coverage, format, lint, mypy and build"
	@echo "  serve-docs     Serve documentation"
	@echo "  help           Show this help message"
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
	@echo "  make serve-docs"
	@echo "  make help"
	@echo ""
	@echo "For more information, see the Makefile"
	@echo ""