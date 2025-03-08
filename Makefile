# Makefile for project management
# Compatible with Windows, macOS, and Linux
.PHONY: update-deps upgrade-deps format lint mypy qa test coverage build test-package check-package serve-docs help

# Variables for cross-platform compatibility
CP = cp
ifeq ($(OS),Windows_NT)
	CP = copy
	# Disable colors on Windows and use echo instead of printf
	RED = 
	GREEN = 
	YELLOW = 
	BLUE = 
	NC = 
	PRINT = echo
else
	# ANSI color codes for non-Windows platforms
	RED = \033[0;31m
	GREEN = \033[0;32m
	YELLOW = \033[0;33m
	BLUE = \033[0;34m
	NC = \033[0m # No Color
	PRINT = printf
endif

# --------------------------------------
# Dependencies
# --------------------------------------

update-deps:
	uv lock --upgrade
	uv sync --all-extras --dev

upgrade-deps: update-deps

# --------------------------------------
# Code Quality
# --------------------------------------

format:
	uv run ruff format

lint:
	uv run ruff check --fix

mypy:
	uv run mypy .

qa: format lint mypy

# --------------------------------------
# Package Testing
# --------------------------------------

test:
	uv pip install -e .
	uv run pytest
	uv run coverage report
	uv run coverage html

build:
	uv build

check-package: build test qa

# --------------------------------------
# Documentation
# --------------------------------------

serve-docs:
	uv run quarto render README.qmd
	$(CP) README.md docs/index.md
	$(CP) CHANGELOG.md docs/changelog.md
	uv run mkdocs build
	uv run mkdocs serve

# --------------------------------------
# Help
# --------------------------------------

help:
	@$(PRINT) "$(BLUE)Usage: make [target]$(NC)"
	@$(PRINT) ""
	@$(PRINT) "$(YELLOW)Available Targets:$(NC)"
	@$(PRINT) "$(GREEN) Dependencies:$(NC)"
	@$(PRINT) "   $(RED)update-deps$(NC)    - Update and sync dependencies"
	@$(PRINT) "   $(RED)upgrade-deps$(NC)   - Alias for update-deps"
	@$(PRINT) ""
	@$(PRINT) "$(GREEN) Code Quality:$(NC)"
	@$(PRINT) "   $(RED)format$(NC)        - Format code using ruff"
	@$(PRINT) "   $(RED)lint$(NC)          - Lint code with ruff and fix issues"
	@$(PRINT) "   $(RED)mypy$(NC)          - Run type checking with mypy"
	@$(PRINT) "   $(RED)qa$(NC)            - Run all quality checks (format, lint, mypy)"
	@$(PRINT) ""
	@$(PRINT) "$(GREEN) Testing & Packaging:$(NC)"
	@$(PRINT) "   $(RED)test$(NC)          - Run tests with pytest"
	@$(PRINT) "   $(RED)coverage$(NC)      - Generate test coverage report"
	@$(PRINT) "   $(RED)build$(NC)         - Build the package"
	@$(PRINT) "   $(RED)test-package$(NC)  - Run tests and coverage"
	@$(PRINT) "   $(RED)check-package$(NC) - Full package check (tests, QA, build)"
	@$(PRINT) ""
	@$(PRINT) "$(GREEN) Documentation:$(NC)"
	@$(PRINT) "   $(RED)serve-docs$(NC)    - Build and serve documentation"
	@$(PRINT) ""
	@$(PRINT) "$(GREEN) Help:$(NC)"
	@$(PRINT) "   $(RED)help$(NC)          - Display this help message"
	@$(PRINT) ""
	@$(PRINT) "$(YELLOW)Examples:$(NC)"
	@$(PRINT) "   make $(RED)test$(NC)          # Run tests"
	@$(PRINT) "   make $(RED)qa$(NC)            # Run all quality checks"
	@$(PRINT) "   make $(RED)check-package$(NC) # Run full package validation"
	@$(PRINT) "   make $(RED)serve-docs$(NC)    # Serve documentation locally"
