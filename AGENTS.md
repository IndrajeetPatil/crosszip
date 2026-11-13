# Agent Instructions

## Single-source docs
- `README.md` is also the documentation homepage: `docs/index.md` only
  includes it via `--8<--`, so edit `README.md`, never `docs/index.md`. Its
  Python examples run in `tests/test_readme.py`, which compares each one's
  output with the fenced block after its `<!--pytest-codeblocks:expected-output-->`
  marker; update that block when a code change alters the output.
- `CHANGELOG.md` is also the documentation changelog page: `docs/changelog.md`
  only includes it via `--8<--`, so edit `CHANGELOG.md`, never
  `docs/changelog.md`. Separate two changelog entries with a blank line, so
  each bullet stands apart from the next.

## Tooling
- Use `uv` for environments and dependencies, not `pip`, `pipenv` or `poetry`,
  and never edit `uv.lock` by hand.
- Use the `Makefile` targets rather than calling the tools directly. `make
  format` applies Ruff's `missing-trailing-comma` fix before `ruff format`,
  so a bare `ruff format` collapses intentional multiline layouts.
- To upgrade dependencies and hooks, follow `.github/prompts/update-deps.md`.
- If `pyrefly` and `ty` disagree on an issue, `ty` wins.

## Checks
- `make check-package` (tests with 100% coverage, QA, build) and
  `make hooks` (`prek` hooks from `prek.toml`) must pass before committing.
- After changing `docs/`, `README.md`, `CHANGELOG.md`, `mkdocs.yml` or a public
  docstring, also run `make build-docs`, a strict build that fails on warnings.
- Reference `IndrajeetPatil/workflows` reusable workflows as `@main`, never a
  commit SHA. The owner maintains them and is the only person who can
  contribute to this repository, so there is no external-contributor risk, and
  `@main` keeps it on the latest version. Code scanners (CodeQL
  `actions/unpinned-tag`, zizmor `unpinned-uses`) flag this by design: do not
  report it or propose a pin; dismiss such alerts as "won't fix" with this
  reason.

## Release Process
To create a new release, follow `.github/prompts/create-release.md` (it covers
the code-scanning alert check).

## Agent Skills
Skills live in `.agents/skills/<name>/SKILL.md`. Load one before its task:

| Skill | Load before |
| --- | --- |
| `mutation-testing` | Running mutmut, acting on surviving mutants or the weekly mutation-test report |
