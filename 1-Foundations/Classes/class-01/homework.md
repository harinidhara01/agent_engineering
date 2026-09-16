# Class 1 Homework

## Starting checkpoint

None — this is the first commit. Work from a fresh, empty repository.

## Required (45–60 minutes)

Finish and commit the merged charter and harness:

- `README.md`, `SPEC.md`, `docs/widgetware-business-brief.md`, `docs/acceptance-criteria.md`, `tests/scenarios/` — the charter, from class.
- `pyproject.toml`, `src/widgetware_sdr/` (health check + `__init__.py`), `scripts/verify_environment.py`, `scripts/check.sh`, `.env.example`, `.gitignore` — the harness, from class.
- `docs/architecture.md` and `docs/architecture-decisions/` — if not finished live, complete these using `golden-solution/`'s versions as a model for depth, but write your own reasoning.

Get `./scripts/check.sh` passing cleanly from a fresh clone before you consider this level done. Use `golden-solution/` as the reference if you get stuck, but write your own version first — the point of this homework is having your own opinion about what these documents and this workspace should contain.

## Diagnostic (targeted fix)

Take one acceptance criterion from your `docs/acceptance-criteria.md` Section A and rewrite it until a stranger could evaluate this checkpoint against it without asking you a clarifying question. A criterion like "the repository is well organized" is not yet testable — what, specifically, would `./scripts/check.sh` or a person actually check?

## Extension (optional)

Complete whichever of these you didn't finish in class:

- `.agents/rules/engineering.md`, `.agents/rules/security.md`, `.agents/workflows/baseline-check.md`
- `CONTRIBUTING.md` and `SECURITY.md`
- One additional disqualifying scenario for `tests/scenarios/`, different in kind from the one covered in class (which failed on industry and size) — for example, an account that fits the ICP on paper but carries an explicit exclusion flag from a past disqualification.

## Submission

- The full repository, committed to your fork.
- Terminal output of `./scripts/check.sh` running clean, from a fresh clone if possible.
- A one-paragraph note identifying which acceptance criterion you rewrote for the Diagnostic level, and what specifically changed.

## Constraints

- No Gemini call, no ADK import, no network call, no send-capable code anywhere in `src/`. `tests/unit/test_repository_contract.py` checks for this automatically — if it fails, something is out of scope for this class.
- No YAML configuration files in `config/` yet — that starts Class 2. `config/README.md` documents why it's empty; leave it that way.
- Do not weaken `verify_environment.py` or `tests/unit/test_repository_contract.py` to make them pass. If a test seems wrong, say so in your submission note instead of silently loosening it.

## What "done" looks like

A stranger can clone your repository, run the documented Quick Start sequence, and get a clean `./scripts/check.sh` pass — and, separately, could read your five charter documents and correctly answer: what does this system do, what will it never do, and how will we know if it's working?
