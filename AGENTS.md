# Agent Instructions

This is a Python package repository following standard development practices.

## Project Structure
- `src/`: Contains the main package code.
- `tests/`: Contains the `pytest` test suite.
- `docs/`: Contains documentation files.
- `pyproject.toml`: The primary configuration file for metadata and tools.
- `uv.lock`: Lockfile ensuring reproducible environments.

## Setup & Dependencies
- We use [`uv`](https://github.com/astral-sh/uv) for fast package and environment management.
- **Do not** use `pip`, `pipenv`, or `poetry` directly.
- **Do not** manually edit `uv.lock`.
- To reproduce the locked environment, run `uv sync`.
- To explicitly upgrade dependencies and pre-commit hooks, run `make update-deps`.

## Code Quality & Testing
- Code formatting and linting are handled by `ruff`, and type checking by `ty`.
- Pre-commit hooks are configured via `prek`.
- **Do not** commit code with linting errors, type warnings, or failing tests.
- Always run `make qa` to format, lint, type-check, and audit dependencies.
- Run `make check-package` to run the full validation suite (QA + Tests + Build).
- **Do not** bypass the `Makefile`; rely on its targets for standardized workflows.

## Contribution Workflow
1. Ensure you are on a feature branch.
2. Implement your code changes within `src/` and corresponding tests within `tests/`.
3. Verify all changes by running `make check-package`.
4. Commit your changes and push to the branch to update the Pull Request.

## Release Process
This package uses automated workflows for publishing to PyPI and GitHub Releases to ensure a reliable and reproducible release mechanism.

1. **Versioning**: The package version is determined by the `version` field in `pyproject.toml`. You MUST update this field and `CHANGELOG.md` appropriately before creating a release.
2. **Triggering a Release**: The release process is entirely automated but triggered manually via GitHub Actions workflow dispatch on the `release.yml` workflow. No manual builds should be published from developer laptops.
3. **Automated Build Steps**:
   - The workflow checks out the code and sets up the `uv` toolchain.
   - It extracts the version directly from `pyproject.toml` using `uv version` to ensure the GitHub tag matches the package version.
   - It installs all build dependencies and builds the package distributions (source distribution `sdist` and wheel `bdist_wheel`) using `uv build`.
4. **Publishing Steps**:
   - **GitHub**: It creates a GitHub Release with a tag exactly matching the version. It attaches the auto-generated release notes based on the PR history and targets the commit from which the workflow was dispatched.
   - **PyPI**: It securely publishes the built `.tar.gz` and `.whl` artifacts to the Python Package Index (PyPI) using `pypa/gh-action-pypi-publish`, which relies on OpenID Connect (OIDC) trusted publishing (no manual tokens are required).
