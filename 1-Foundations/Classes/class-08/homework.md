# Class 8 Homework

## Starting checkpoint

`../class-07/golden-solution/` (or your own Class 7 submission)

## Required (30–45 minutes)

1. Build `workflow/state_machine.py`, `workflow/approval.py`, `workflow/coordinator.py`, `contracts/evidence_review.py`, `contracts/outreach_draft.py`, and the two new agents.
2. Get all five required scenario tests passing: success, insufficient evidence, source conflict, malformed output, rejected approval.
3. Run the full workflow for at least two accounts and confirm each one resumes correctly from a checkpoint after a simulated interruption (stop the process, restart, read the checkpoint file back).

## Diagnostic (targeted fix)

The provided rejected-approval test currently confirms `record_approval_decision(REJECT)` returns `REJECTED`, but nothing checks that this is actually a *legal* transition from wherever the run currently sits. Strengthen the test to call `validate_transition(run.state, WorkflowState.REJECTED)` and assert it's true — and explain, in one sentence, what a passing "returns REJECTED" test with a *failing* `validate_transition` check would actually mean.

## Extension (optional)

Add a sixth partial-failure scenario from §9.7's list not covered in class (research source unavailable, user rejects the draft, workflow resumed after interruption) with its own test, following the same "visible state, prior work preserved" pattern as the five required ones.

## Submission

- `./scripts/check.sh` output, all green.
- Terminal output of a resumed-from-checkpoint run.
- A `grep -ri "send\|smtp\|email.*send" src/` output, to show, live, that no send-capable code exists anywhere in the codebase.

## Constraints

- The workflow must terminate at `AWAITING_APPROVAL` or a named failure state — never anything resembling "sent."
- The Drafting Agent must never receive the raw `ResearchBrief` — only the `EvidenceReview`'s approved claims.

## What "done" looks like

You can kill the workflow mid-run, on purpose, and prove — not just claim — that the research already completed survives the interruption.
