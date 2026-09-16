# Class 10 Grading Criteria

Used with `../GRADING-RUBRIC-TEMPLATE.md`. These are the criteria specific to this class — the things `pytest` cannot check, or can only check for the specific cases already anticipated.

1. **The single-account workflow is verifiably untouched.** A submission should be able to show (via `git diff` or a direct file comparison) that `run_workflow` and everything it calls have zero changes from Class 9. If they changed, ask why — the answer should never be "to make the loop work."

2. **The new loop states attach to the state machine with real justification, not just to make a test pass.** Ask why `RETRY_PENDING` transitions back to `RESEARCHING` specifically, and why `NEEDS_HUMAN_REVIEW` is terminal from the loop's own perspective. A submission that can't explain these choices copied the shape without the reasoning.

3. **The five-way decision function's branches are each individually tested.** A submission with tests only for CONTINUE and STOP, and no test forcing RETRY, DEFER, or ESCALATE, hasn't proven the decision logic — those three are exactly the cases most likely to have a subtle bug.

4. **The `LoopAgent` deprecation warning (if the submitter's ADK version shows one) is investigated, not suppressed.** Check whether test output was captured with warnings visible, and whether the submission's own notes mention it. Silently filtering warnings to get a "clean" test run, without reading what the warning says, is exactly the habit this course is trying to prevent.

5. **The batch loop's budget-tracking claim is honest about what it measures.** If a submission's `KNOWN_FAILURE_CASES.md` (or equivalent) doesn't note any coarse proxy used for tracking usage against a budget (e.g., counting per-account rather than per-tool-call), that's a real gap in self-awareness, not just documentation.

6. **Approval scrutiny genuinely doesn't relax inside the loop.** Trace one account through the batch loop that should land at `AWAITING_APPROVAL` and confirm nothing in the loop code auto-approves it or skips the state. This is the single most important property of the whole chapter.

7. **Independent understanding, not a copy.** If the submission's state-machine extension and loop are near-identical to the gold reference in wording and structure with no evidence of independent construction, note that explicitly per the anti-gaming guidance in the generic template.
