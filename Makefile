# Makefile for project management
# Compatible with Windows, macOS, and Linux
.PHONY: update-deps upgrade-deps format lint mypy qa test coverage build test-package check-package serve-docs help

# Variables for cross-platform compatibility
CP = cp
ifeq ($(OS),Windows_NT)
	CP = copy
endif

# ANSI color codes
RED = \033[0;31m
GREEN = \033[0;32m
YELLOW = \033[0;33m
BLUE = \033[0;34m
NC = \033[0m # No Color

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
	@printf "$(BLUE)Usage: make [target]$(NC)\n"
	@printf "\n"
	@printf "$(YELLOW)Available Targets:$(NC)\n"
	@printf "$(GREEN) Dependencies:$(NC)\n"
	@printf "   $(RED)update-deps$(NC)    - Update and sync dependencies\n"
	@printf "   $(RED)upgrade-deps$(NC)   - Alias for update-deps\n"
	@printf "\n"
	@printf "$(GREEN) Code Quality:$(NC)\n"
	@printf "   $(RED)format$(NC)        - Format code using ruff\n"
	@printf "   $(RED)lint$(NC)          - Lint code with ruff and fix issues\n"
	@printf "   $(RED)mypy$(NC)          - Run type checking with mypy\n"
	@printf "   $(RED)qa$(NC)            - Run all quality checks (format, lint, mypy)\n"
	@printf "\n"
	@printf "$(GREEN) Testing & Packaging:$(NC)\n"
	@printf "   $(RED)test$(NC)          - Run tests with pytest\n"
	@printf "   $(RED)coverage$(NC)      - Generate test coverage report\n"
	@printf "   $(RED)build$(NC)         - Build the package\n"
	@printf "   $(RED)test-package$(NC)  - Run tests and coverage\n"
	@printf "   $(RED)check-package$(NC) - Full package check (tests, QA, build)\n"
	@printf "\n"
	@printf "$(GREEN) Documentation:$(NC)\n"
	@printf "   $(RED)serve-docs$(NC)    - Build and serve documentation\n"
	@printf "\n"
	@printf "$(GREEN) Help:$(NC)\n"
	@printf "   $(RED)help$(NC)          - Display this help message\n"
	@printf "\n"
	@printf "$(YELLOW)Examples:$(NC)\n"
	@printf "   make $(RED)test$(NC)          # Run tests\n"
	@printf "   make $(RED)qa$(NC)            # Run all quality checks\n"
	@printf "   make $(RED)check-package$(NC) # Run full package validation\n"
	@printf "   make $(RED)serve-docs$(NC)    # Serve documentation locally\n"
