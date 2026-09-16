# Contributing

This repository is a teaching checkpoint, not an open-source project accepting outside contributions — but every change to it, yours or Antigravity's, should go through the same disciplined cycle.

## Before proposing a change

1. State the objective in one sentence: what repository outcome are you trying to produce?
2. Identify which files are in scope. If the change touches `SPEC.md` or the business brief, stop — those define the system's contract and shouldn't shift casually alongside an unrelated implementation task.
3. Know your acceptance criteria before you start. "It looks right" is not one.

## The review cycle

State objective → provide the relevant spec → ask for a plan → review the plan → permit bounded implementation → inspect the diff → run `./scripts/check.sh` → accept, revise, or revert.

Do not skip the plan-review step because a task looks small. A generated diff that quietly does more than what was asked is the most common way scope creep enters a codebase like this one — see `docs/architecture-decisions/0001-bounded-autonomy.md` for why that specifically matters here.

## Before every commit

- `./scripts/check.sh` passes, from a clean environment if you have any doubt.
- No secret, API key, or credential value appears in any tracked file — `git diff --staged` and read it, don't assume.
- The commit message states the behavior established, not just the files touched.

## Code style

- Plain, explicit Python. Prefer a small function with a clear name over a clever one-liner.
- Type annotations on every function signature — `mypy src tests scripts` is part of the gate, not optional.
- No dependency addition without a stated reason. The standard library is the default; a new package is a decision, not a convenience.
