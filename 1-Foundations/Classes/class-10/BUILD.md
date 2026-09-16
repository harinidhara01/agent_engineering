# Building Class 10 with Antigravity

Goal: wrap the Class 9 workflow, unchanged, in a bounded ADK loop that processes a queue of accounts unattended. `golden-solution/` in this folder is the reference. Build your own copy in `my-work/gemini-book-1/class-10/`, then diff.

## Prerequisites

- **`../SETUP.md` complete.**
- Your Class 9 checkpoint, passing `./scripts/check.sh`, including a passing release gate.

## Steps

1. Extend `workflow/state_machine.py` with `RETRY_PENDING` and `NEEDS_HUMAN_REVIEW`. Decide where they attach to the existing transition table yourself before looking at the reference — Book 1 §11.6 tells you what the two states mean, not which existing state should route to them. `BLOCKED` should no longer be terminal once you're done.

2. Write `loop/budget.py`, `loop/decision.py` (the five-way decision — CONTINUE, RETRY, STOP, DEFER, ESCALATE), `loop/account_queue.py`, and `loop/run_report.py`.

3. Write `loop/batch_runner.py`'s `run_batch()` to accept `qualify`/`review`/`draft` as injected callables, exactly like Class 8's `run_workflow` — this keeps the whole loop testable offline. Checkpoint after every account, and verify the state the workflow actually reached (§11.7) before deciding what to do next.

4. Ask Antigravity for the ADK-native `LoopAgent` wiring, but expect a surprise:

   > "Write `create_batch_loop_agent()`, wrapping the WidgetWare workflow in a `google.adk.agents.LoopAgent` with a configurable `max_iterations`."

   If your installed `google-adk` version prints a deprecation warning about `LoopAgent`, don't ignore it or hide it — read what it says, and document it honestly in your own `KNOWN_FAILURE_CASES.md`. The book teaches the concept correctly; the SDK underneath it may have moved since the book was written, and noticing that is itself the discipline this course is trying to build.

5. Build a four-account seed queue, at least one outside WidgetWare's ICP, and run the full batch loop against it. Write tests for: a fresh account gets selected, a settled one doesn't, a recoverable failure retries up to the limit and no further, the loop stops at every declared budget, and every run names a stop reason.

6. Double-check that whatever counter your budget check reads against is actually incremented somewhere in the loop — a budget stop condition that's never triggered because nothing ever increments the counter it checks is a real, easy-to-miss bug class, not a hypothetical.

## Verify

```
cd my-work/gemini-book-1/class-10
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
./scripts/check.sh
```

All loop tests should pass offline.

## Compare against the reference

`golden-solution/tests/loop/test_batch_runner.py` is the reference for the full loop scenario suite. Pay attention to how its `review` stub — not the coordinator — is what actually stops a disqualified account from reaching `AWAITING_APPROVAL`; if your own test suite doesn't model that, you may be relying on the coordinator to do something it was never designed to do.

## Grade it

Passing tests proves the loop mechanics are correct. It doesn't prove your loop's budgets are set to sensible real-world values, or that the new states attach to the state machine for a real reason rather than just to make a test pass. Run the quality check: `GRADING.md` in this folder plus `../GRADING-RUBRIC-TEMPLATE.md`.
