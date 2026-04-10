# Review Process

This project has both code and textbook content, and review takes both seriously. This document describes how contributions are reviewed before they are merged into `main`.

## Review Tiers

Different kinds of changes need different levels of review.

| Change type | Reviewers | Required approvals |
|---|---|---|
| Typo / grammar fix in prose | 1 reviewer | 1 |
| Code bug fix in `kanto_utils` | 1 reviewer with statistics background | 1 |
| New notebook exercise | 1 reviewer | 1 |
| New textbook section or concept | 2 reviewers (1 statistics, 1 pedagogy) | 2 |
| Changes to data generating process | 2 reviewers (1 statistics, 1 code) | 2 |
| Changes to causal estimators in `kanto_utils.causal` | 2 reviewers (1 statistics, 1 code) + unit tests | 2 |
| New chapter | 3 reviewers (2 statistics, 1 pedagogy) | 3 |

## Pull Request Checklist

Before submitting a PR, every contributor must work through the checklist in the PR template (see `.github/PULL_REQUEST_TEMPLATE.md`). Reviewers verify each item.

### For all PRs

- [ ] Branch is up to date with `main`
- [ ] Commit messages follow conventional commits (`feat:`, `fix:`, `docs:`, `refactor:`, `test:`)
- [ ] No sensitive files (`.env`, keys, credentials) are staged
- [ ] CI is green (test, notebook validation, PDF build)
- [ ] `CHANGELOG.md` is updated under the unreleased section

### For code changes

- [ ] Type hints on public functions
- [ ] Docstrings on public functions and classes
- [ ] Unit tests cover the new behavior
- [ ] No silent exception handling — errors surface or are explicitly documented
- [ ] `seed=151` is preserved in any new random operations
- [ ] `pytest` passes locally (`pytest tests/`)

### For notebook changes

- [ ] Notebook runs top-to-bottom without errors
- [ ] All cells have expected outputs cleared before commit (`jupyter nbconvert --clear-output`)
- [ ] Narrative matches the corresponding textbook chapter
- [ ] Exercises include hints and solutions in spoiler tags or a separate cell

### For textbook content

- [ ] Math notation matches Appendix A conventions
- [ ] Every new concept has: (1) intuition via Pokemon analogy, (2) formal definition, (3) worked example
- [ ] New terms are added to the glossary (Appendix D)
- [ ] Citations are real papers with author/year/venue
- [ ] Claims are supported by citations or simulation results from the companion notebook
- [ ] LaTeX compiles cleanly (`make -C textbook/build pdf`)

## Statistical Review

Changes to causal estimators, data generating processes, or any mathematical claims require a statistical reviewer. A statistical review checks:

1. **Identification.** Is the stated causal effect actually identified under the assumptions given?
2. **Estimation.** Is the estimator consistent for the target parameter? Is variance correctly computed?
3. **Simulation.** Does the companion notebook demonstrate the method works on simulated data where the truth is known?
4. **Assumptions.** Are the assumptions stated clearly and are their violations discussed?
5. **Literature.** Does the presentation align with the standard references in the field?

## Pedagogical Review

New textbook content also receives a pedagogical review that checks:

1. **Prerequisites.** Does the content assume only things readers have seen earlier in the book?
2. **Scaffolding.** Do difficult concepts build from intuition to formalism?
3. **Exercises.** Are the exercises at the right difficulty for the chapter's tier?
4. **Clarity.** Can a motivated student at the target level follow the exposition without outside help?
5. **Motivation.** Is the Pokemon framing used to teach, not just to decorate?

## Automated Checks (CI)

Every PR triggers three GitHub Actions workflows:

1. **`test.yml`** runs `pytest` on Python 3.10, 3.11, and 3.12. All unit tests must pass.
2. **`validate_notebooks.yml`** executes every notebook under `notebooks/` with a 600-second timeout. Any notebook that errors fails the PR.
3. **`build_pdf.yml`** builds the full textbook PDF and HTML. The build must succeed and artifacts are uploaded for preview.

A PR cannot merge until all three workflows are green.

## Review Turnaround

| Priority | Target first response | Target merge |
|---|---|---|
| Critical bug (incorrect math, broken CI) | 24 hours | 72 hours |
| Standard contribution | 1 week | 2 weeks |
| Large addition (new chapter) | 2 weeks | 1 month |

Contributors can ping reviewers if a PR has been idle past these targets.

## Becoming a Reviewer

Anyone who has contributed at least three merged PRs and whose work has been of consistently high quality may be nominated as a reviewer. Nominations happen via an issue in this repository.

## Code of Conduct

Reviews are about the work, not the person. Reviewers give specific, actionable feedback. Contributors receive criticism gracefully and revise. Everyone assumes good faith. See [CONTRIBUTING.md](CONTRIBUTING.md) for more.
