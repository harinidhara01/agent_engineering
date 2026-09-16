# Known Failure Cases — Class 9 Checkpoint

## Carried forward from Classes 1–8

- Coordinator scenario tests still use stub `qualify`/`review`/`draft` functions, not the real agents.
- `research.py`'s conflict detection is still one narrow regular expression.

## New at this checkpoint

### 1. The golden dataset is four accounts covering ten categories

`eval/golden_dataset.py`'s ten `GoldenCase` entries reuse only four underlying accounts. `test_every_required_category_has_at_least_one_case` proves every category is *represented*, not that it's adequately *covered* — one case per category is the minimum Book 1 §10.3 asks for, not a claim of statistical confidence.

### 2. `approval_compliance_rate` only recognizes the states that exist at this checkpoint

This function's "compliant" set currently lists `AWAITING_APPROVAL`, `APPROVED`, `REJECTED`, and `BLOCKED` — the four terminal-or-waiting states Chapter 9's workflow can reach. Class 10 adds `RETRY_PENDING` and `NEEDS_HUMAN_REVIEW` to the state machine; this function will need updating then, or it will silently undercount compliant runs inside a batch loop. Flagged here explicitly so that update isn't missed.

### 3. There is no loop yet — this checkpoint evaluates one account at a time, run on request

That's the deliberate scope of this chapter: prove the single-account workflow is good enough to ship *before* automating it. If you're looking for a way to process a queue of accounts unattended, that's Class 10, not here — and the manuscript's own ordering argument is that building it here, before evaluation, would be building on an unproven foundation.

### 4. `check_release_gate`'s thresholds are placeholders, not calibrated numbers

`SCENARIO_PASS_THRESHOLD = 0.95` and `EVIDENCE_COVERAGE_THRESHOLD = 1.0` are reasonable-looking defaults, not numbers derived from any real production data — there is none yet. Treat them as a starting point to revisit once real traffic exists (which doesn't happen until Book 2's continuous-evaluation chapter).
