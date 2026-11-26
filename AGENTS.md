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

- After changing `docs/`, `README.md`, `CHANGELOG.md`, `mkdocs.yml`, or a
  public docstring, also run `make build-docs`, a strict build that fails on
  warnings.

- Reference `IndrajeetPatil/workflows` reusable workflows as `@main`, never a
  commit SHA. The owner maintains them and is the only person who can
  contribute to this repository, so there is no external-contributor risk, and
  `@main` keeps it on the latest version. Code scanners (CodeQL
  `actions/unpinned-tag`, zizmor `unpinned-uses`) flag this by design: do not
  report it or propose a pin; dismiss such alerts as "won't fix" with this
  reason.

- The benchmarks in `tests/benchmarks/` back a CI regression gate; see its
  `README.md`.

## Release Process
To create a new release, follow `.github/prompts/create-release.md` (it covers
the code-scanning alert check).

## Agent Skills
Skills live in `.agents/skills/<name>/SKILL.md`. Load one before its task:

| Skill | Load before |
| --- | --- |
| `mutation-testing` | Running mutmut, acting on surviving mutants or the weekly mutation-test report |

## Learn from mistakes

When a check fails, a reviewer raises a finding, or you notice a mistake in
your own work, fix it, then ask what led you to it. If `AGENTS.md`, a skill,
its scripts or templates, a prompt, or a doc gave missing, ambiguous, or
wrong guidance, correct that guidance in the same pull request, stating the
general rule rather than the incident. Never weaken a quality gate instead.

## Pull requests

Follow these rules without relying on any instructions outside this
repository:

- Write every commit message and PR title as a Conventional Commit,
  `type(scope): description`, lowercase and imperative, with an allowed type
  (`build`, `chore`, `ci`, `docs`, `feat`, `fix`, `perf`, `refactor`,
  `revert`, `style`, `test`). Keep the PR title and body in sync with the
  net diff.

- Open every PR ready for review with `gh pr create`, never as a draft.

- Never add agent or tool attribution to commits, PRs, or comments.

- After opening or pushing, wait for hosted CI to finish. Inspect failed jobs,
  fix the cause, run the local checks (`make check` and `make hooks`), push,
  and repeat. Every check must pass, not just the required ones: a failing,
  queued, or skipped check is not success, and a rerun that fails again is
  not an explanation.

- If an automatic AI review (Codex, for the owner) runs on the PR, wait for
  its result instead of requesting one. Fix merited findings, reply to and
  resolve addressed threads, and continue until the review approves the
  current head with no unresolved findings. Never write `@codex` anywhere in
  a PR, even in backticks: it cancels the automatic review. Say "a Codex
  review request" instead.

- If Codex reports exhausted usage, leave the PR open and report it; no other
  reviewer or silence counts as approval. Once usage refreshes, comment
  `@codex review` once; only this case needs the comment.

- Once every check passes and the review gate is met, squash-merge, then
  verify the merged state. Recheck the head, threads, and checks immediately
  before merging, and never bypass branch protections. A CodSpeed regression
  blocks merging until it is investigated, and acknowledged in CodSpeed only
  when intentional or shown to be unrelated to the change.

- Update a PR branch from `main` only to resolve conflicts or pick up a change
  the PR depends on, never just to bring it up to date.

- Report local validation, hosted CI, review, and merge state separately,
  naming every failing check, required or not. If an external blocker stops
  completion, leave the PR open and say so.
