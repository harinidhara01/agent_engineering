# Workflow: Baseline Check

A reusable procedure for verifying this checkpoint from a clean state. Invoke this workflow whenever you need to confirm the repository is healthy — before starting new work, after accepting a generated diff, or before declaring a task complete.

## Steps

1. Confirm a virtual environment is active (`which python3` should point inside `.venv/`). If not, create and activate one:
   ```bash
   python3 -m venv .venv && source .venv/bin/activate
   ```
2. Install the project with development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
3. Run the full gate:
   ```bash
   ./scripts/check.sh
   ```
4. Report the actual output of step 3 — every stage's pass/fail status, not a summary claim. A task is not complete until this workflow has been run and its real output captured.

## When this workflow fails

- **`verify_environment.py` fails** — read its specific message; it names exactly which check failed and why. Do not proceed to the remaining steps until it passes.
- **Formatting or lint fails** — run `ruff format .` to fix formatting automatically, then re-run; lint failures usually need a manual look at what `ruff check .` reports.
- **`mypy` fails** — a missing or incorrect type annotation. Fix the annotation; do not silence with a blanket `# type: ignore` unless the underlying issue is genuinely outside this codebase's control, and say so in a comment if you do.
- **A test fails** — this is real information about the codebase, not the workflow. Diagnose before changing the test to make it pass.

## Do not

- Skip a step to "save time." The whole point of one command running all steps in order is that skipping one silently narrows what "all checks passed" actually means.
- Report success without having actually run this workflow in the current state of the repository.
