# Makefile for project management
# Compatible with Windows, macOS, and Linux
.PHONY: update-deps upgrade-deps format lint mypy qa test-coverage build test-package check-package serve-docs help

# Variables for cross-platform compatibility
CP = cp
ECHO = echo
ifeq ($(OS),Windows_NT)
	CP = copy
	ECHO = cmd /c echo.
endif

# ANSI color codes
RED = \033[0;31m
GREEN = \033[0;32m
YELLOW = \033[0;33m
BLUE = \033[0;34m
NC = \033[0m # No Color

# Plain text fallbacks for no-color environments
RED_PLAIN = 
GREEN_PLAIN = 
YELLOW_PLAIN = 
BLUE_PLAIN = 
NC_PLAIN = 

# Detect if terminal supports colors (Windows-specific check)
ifeq ($(OS),Windows_NT)
	# Check if running in a modern terminal (e.g., Windows Terminal)
	ifneq ($(findstring Windows Terminal,$(shell echo %TERM%)),Windows Terminal)
		RED = $(RED_PLAIN)
		GREEN = $(GREEN_PLAIN)
		YELLOW = $(YELLOW_PLAIN)
		BLUE = $(BLUE_PLAIN)
		NC = $(NC_PLAIN)
	endif
endif

# --------------------------------------
# Dependencies
# --------------------------------------

update-deps:
	uv lock --upgrade
	uv sync

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

test-coverage:
	uv run coverage run -m pytest .
	uv run coverage report
	uv run coverage html

build:
	uv build

test-package: test-coverage

check-package: test-package qa build

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
	@$(ECHO) $(BLUE)Usage: make [target]$(NC)
	@$(ECHO) 
	@$(ECHO) $(YELLOW)Available Targets:$(NC)
	@$(ECHO) $(GREEN) Dependencies:$(NC)
	@$(ECHO)    $(RED)update-deps$(NC)    - Update and sync dependencies
	@$(ECHO)    $(RED)upgrade-deps$(NC)   - Alias for update-deps
	@$(ECHO) 
	@$(ECHO) $(GREEN) Code Quality:$(NC)
	@$(ECHO)    $(RED)format$(NC)        - Format code using ruff
	@$(ECHO)    $(RED)lint$(NC)          - Lint code with ruff and fix issues
	@$(ECHO)    $(RED)mypy$(NC)          - Run type checking with mypy
	@$(ECHO)    $(RED)qa$(NC)            - Run all quality checks (format, lint, mypy)
	@$(ECHO) 
	@$(ECHO) $(GREEN) Testing and Packaging:$(NC)
	@$(ECHO)    $(RED)test-coverage$(NC)  - Run tests and generate coverage report
	@$(ECHO)    $(RED)build$(NC)         - Build the package
	@$(ECHO)    $(RED)test-package$(NC)  - Run tests and coverage
	@$(ECHO)    $(RED)check-package$(NC) - Full package check (tests, QA, build)
	@$(ECHO) 
	@$(ECHO) $(GREEN) Documentation:$(NC)
	@$(ECHO)    $(RED)serve-docs$(NC)    - Build and serve documentation
	@$(ECHO) 
	@$(ECHO) $(GREEN) Help:$(NC)
	@$(ECHO)    $(RED)help$(NC)          - Display this help message
	@$(ECHO) 
	@$(ECHO) $(YELLOW)Examples:$(NC)
	@$(ECHO)    make $(RED)test-coverage$(NC)  # Run tests and coverage
	@$(ECHO)    make $(RED)qa$(NC)            # Run all quality checks
	@$(ECHO)    make $(RED)check-package$(NC) # Run full package validation
	@$(ECHO)    make $(RED)serve-docs$(NC)    # Serve documentation locally
	@if "$(NC)" == "" ( $(ECHO) Note: Colors not supported in this terminal. Use Windows Terminal or Git Bash for colored output.) else ( $(ECHO) )
