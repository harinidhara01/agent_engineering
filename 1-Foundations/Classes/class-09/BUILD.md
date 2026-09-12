# Building Class 9 with Antigravity

Goal: a golden dataset, deterministic metrics, and a release gate that together give a mechanical, repeatable answer to "is this system good enough to ship right now?" `golden-solution/` in this folder is the reference. Build your own copy in `my-work/gemini-book-1/class-09/`, then diff.

## Prerequisites

- **`../SETUP.md` complete.** This class is fully offline — evaluation itself never calls a model; the workflow it evaluates uses deterministic stub agents in tests.
- Your Class 8 checkpoint, passing `./scripts/check.sh`.

## Steps

1. Write `eval/golden_dataset.py` yourself, by hand, before asking Antigravity for anything — deciding what belongs in a golden dataset is the actual thinking this chapter asks for, not something to delegate. Define `GoldenCase` (account, expected outcome category, and enough detail to run it through the real workflow) and `GOLDEN_DATASET`: at minimum one case each for qualified, disqualified, ambiguous/needs-research, conflicting-evidence, and injection-attempt — reusing the fixture accounts already in the repo where they fit.

2. Write `eval/metrics.py`: functions that take a batch of completed `WorkflowRun`s and compute deterministic numbers — a qualification-accuracy rate against expected outcomes, and `approval_compliance_rate()` (the fraction of runs that correctly stopped at `AWAITING_APPROVAL` rather than skipping it). Be explicit in a docstring or comment about which workflow states `approval_compliance_rate()` currently recognizes — at this checkpoint, only the four that exist through Class 8.

3. Ask Antigravity for the release gate, but be explicit about the "fails loudly" requirement — this is the part a generic prompt will get wrong by default:

   > "Write `eval/release_gate.py`'s `check_release_gate(golden_dataset, run_workflow_fn, thresholds) -> ReleaseGateResult`. It must run every case in the golden dataset through the workflow, compare actual to expected outcomes, and compute metrics. `ReleaseGateResult` has `passed: bool` and `reasons: list[str]`. Critically: if multiple things are wrong, `reasons` must contain all of them — never stop at the first failure and never silently swallow a failing case."

4. Write `eval/observability.py`: structured logging for each golden-dataset run (case ID, expected vs. actual outcome, pass/fail) sufficient to reconstruct why a case failed after the fact without re-running it.

5. Write the tests: one per required category confirming the golden case produces its expected outcome, a deliberate-breakage test (mutate one business rule, confirm the gate fails with the right named reason), and a multi-breakage test (break two unrelated things, confirm both reasons appear in one run).

## Verify

```
cd my-work/gemini-book-1/class-09
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
./scripts/check.sh
```

Expect all golden-dataset, metrics, and release-gate tests to pass offline.

## Compare against the reference

`golden-solution/tests/eval/test_release_gate.py` is the reference for what "reports every failure" actually means — in particular, its multi-breakage test. If your release gate's test suite only ever breaks one thing at a time, you haven't proven the "fails loudly, completely" requirement, only the "fails" part.

## Grade it

Passing tests proves the gate mechanically works. It doesn't prove the golden dataset's ten cases are actually representative of what WidgetWare will see in practice, or that the gate's thresholds are calibrated to a real bar rather than whatever happened to be easy to satisfy. Run the quality check: `GRADING.md` in this folder plus `../GRADING-RUBRIC-TEMPLATE.md`.
