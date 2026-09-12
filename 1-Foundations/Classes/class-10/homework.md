# Class 10 Homework

## Starting checkpoint

`../class-09/golden-solution/` (or your own Class 9 submission)

## Required (30–45 minutes)

1. Extend `workflow/state_machine.py` with `RETRY_PENDING` and `NEEDS_HUMAN_REVIEW`, and make `BLOCKED` route to one of them instead of being terminal.
2. Build `loop/budget.py`, `loop/decision.py`, `loop/account_queue.py`, `loop/run_report.py`, and `loop/batch_runner.py`.
3. Run the batch loop against a four-account seed queue (at least one account outside WidgetWare's ICP) and produce a run report naming its `stop_reason`.
4. Get `./scripts/check.sh` passing, offline tests included.

## Diagnostic (targeted fix)

The provided budget test suite currently verifies that a single account's retries count correctly against that *account's own* attempt limit, but does not verify that one badly-behaved account's retries don't quietly consume the *run's* `max_consecutive_failures` budget in a way that stops the whole batch prematurely for everyone else. Write a test with one account that fails twice (using up `max_attempts_per_account`) followed by three healthy accounts, and confirm all three healthy accounts still get processed.

## Extension (optional)

Add a fifth account to the seed queue specifically designed to trigger `DEFER` — you'll need to actually wire a `dependency_available=False` path into `run_batch` for at least one realistic condition (for example: the account's research source returns zero evidence items, treated as a temporarily unavailable dependency rather than automatically `BLOCKED`). Confirm the deferred account is not discarded and would be eligible again on a subsequent run.

## Submission

- `./scripts/check.sh` output, all green.
- One full batch-loop run report (`stop_reason` and `status_totals`).
- One paragraph: which of the five decision outcomes (CONTINUE, RETRY, STOP, DEFER, ESCALATE) was hardest to write a convincing test for, and why.

## Constraints

- Nothing about the single-account workflow (`run_workflow`) changes in this chapter — the loop wraps it, it does not modify it.
- Still no send tool anywhere in the codebase — confirm this with the same grep used in Class 8's homework.

## What "done" looks like

You can run the batch loop against a queue with a mix of qualifying, disqualifying, and unresearchable accounts, and get back a report that honestly explains what happened to each one — including the ones that needed a human. That's Book 1, complete.
