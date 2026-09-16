# Class 9 Homework

## Starting checkpoint

`../class-08/golden-solution/` (or your own Class 8 submission)

## Required (30–45 minutes)

1. Build `eval/golden_dataset.py` with `GOLDEN_DATASET` covering all required categories (qualified, disqualified, ambiguous, conflicting-evidence, injection-attempt, and the rest).
2. Build `eval/metrics.py` with deterministic metrics computed from a batch of workflow runs.
3. Build `eval/release_gate.py`'s `check_release_gate(...)` — it must correctly pass a healthy system and fail an unhealthy one, with every unmet condition named.
4. Get `./scripts/check.sh` passing, including a test that deliberately breaks a business rule and confirms the gate catches it.

## Diagnostic (targeted fix)

The provided release gate currently stops evaluating after the first golden-dataset case fails, instead of running all ten and reporting every failure. Find the early-return (or equivalent short-circuit) responsible, fix it so a single run always reports the complete picture, and write a test that would have caught the original bug — one that deliberately breaks two unrelated things at once and confirms both show up in the result.

## Extension (optional)

Add an eleventh golden-dataset case of your own devising that covers a realistic WidgetWare scenario none of the existing ten categories represent. Show, with a before/after test, that it changes the gate's outcome when the corresponding behavior is deliberately broken — an extension case that can't actually fail anything isn't testing anything.

## Submission

- `./scripts/check.sh` output showing all offline tests passing.
- One full `ReleaseGateResult` output showing a deliberately broken system correctly failing with all reasons named.
- One paragraph: which required category was hardest to write a convincing golden-dataset case for, and why.

## Constraints

- No loop yet — this checkpoint evaluates a single run of the workflow per golden-dataset case, not a batch or retry loop. Class 10 adds the loop.
- The golden dataset must be checked into the repository as code/data, not generated dynamically at test time.

## What "done" looks like

You can hand someone else's deliberately broken checkpoint to `check_release_gate()` and get back a result that names every real problem, with nothing left for them to discover the hard way on a second run.
