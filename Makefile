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
	pre-commit autoupdate

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
ifeq ($(OS),Windows_NT)
	@echo $(BLUE)Usage: make [target]$(NC)
	@echo.
	@echo $(YELLOW)Available Targets:$(NC)
	@echo $(GREEN) Dependencies:$(NC)
	@echo     $(RED)update-deps$(NC)    - Update and sync dependencies
	@echo     $(RED)upgrade-deps$(NC)   - Alias for update-deps
	@echo.
	@echo $(GREEN) Code Quality:$(NC)
	@echo     $(RED)format$(NC)        - Format code using ruff
	@echo     $(RED)lint$(NC)          - Lint code with ruff and fix issues
	@echo     $(RED)mypy$(NC)          - Run type checking with mypy
	@echo     $(RED)qa$(NC)            - Run all quality checks (format, lint, mypy)
	@echo.
	@echo $(GREEN) Testing and Packaging:$(NC)
	@echo     $(RED)test-coverage$(NC) - Run tests and generate coverage report
	@echo     $(RED)build$(NC)         - Build the package
	@echo     $(RED)test-package$(NC)  - Run tests and coverage
	@echo     $(RED)check-package$(NC) - Full package check (tests, QA, build)
	@echo.
	@echo $(GREEN) Documentation:$(NC)
	@echo     $(RED)serve-docs$(NC)    - Build and serve documentation
	@echo.
	@echo $(GREEN) Help:$(NC)
	@echo     $(RED)help$(NC)          - Display this help message
	@echo.
	@echo $(YELLOW)Examples:$(NC)
	@echo     make $(RED)test-coverage$(NC)  # Run tests and coverage
	@echo     make $(RED)qa$(NC)            # Run all quality checks
	@echo     make $(RED)check-package$(NC) # Run full package validation
	@echo     make $(RED)serve-docs$(NC)    # Serve documentation locally
else
	@printf "$(BLUE)Usage: make [target]$(NC)\n"
	@printf "\n"
	@printf "$(YELLOW)Available Targets:$(NC)\n"
	@printf "$(GREEN) Dependencies:$(NC)\n"
	@printf "    $(RED)update-deps$(NC)    - Update and sync dependencies\n"
	@printf "    $(RED)upgrade-deps$(NC)   - Alias for update-deps\n"
	@printf "\n"
	@printf "$(GREEN) Code Quality:$(NC)\n"
	@printf "    $(RED)format$(NC)        - Format code using ruff\n"
	@printf "    $(RED)lint$(NC)          - Lint code with ruff and fix issues\n"
	@printf "    $(RED)mypy$(NC)          - Run type checking with mypy\n"
	@printf "    $(RED)qa$(NC)            - Run all quality checks (format, lint, mypy)\n"
	@printf "\n"
	@printf "$(GREEN) Testing and Packaging:$(NC)\n"
	@printf "    $(RED)test-coverage$(NC)  - Run tests and generate coverage report\n"
	@printf "    $(RED)build$(NC)         - Build the package\n"
	@printf "    $(RED)test-package$(NC)  - Run tests and coverage\n"
	@printf "    $(RED)check-package$(NC) - Full package check (tests, QA, build)\n"
	@printf "\n"
	@printf "$(GREEN) Documentation:$(NC)\n"
	@printf "    $(RED)serve-docs$(NC)    - Build and serve documentation\n"
	@printf "\n"
	@printf "$(GREEN) Help:$(NC)\n"
	@printf "    $(RED)help$(NC)          - Display this help message\n"
	@printf "\n"
	@printf "$(YELLOW)Examples:$(NC)\n"
	@printf "    make $(RED)test-coverage$(NC)  # Run tests and coverage\n"
	@printf "    make $(RED)qa$(NC)             # Run all quality checks\n"
	@printf "    make $(RED)check-package$(NC)  # Run full package validation\n"
	@printf "    make $(RED)serve-docs$(NC)     # Serve documentation locally\n"
endif
