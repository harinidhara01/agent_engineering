# Class 5 Homework

## Starting checkpoint

`../class-04/golden-solution/` (or your own Class 4 submission)

## Required (30–45 minutes)

1. Build `src/widgetware_sdr/contracts/evidence.py` (`EvidenceItem`) and `src/widgetware_sdr/contracts/qualification.py` (`QualificationResult`), both Pydantic v2 models with `extra="forbid"`.
2. Implement all four business invariants as a `@model_validator(mode="after")`: `QUALIFIED` needs `evidence_refs`, `NOT_QUALIFIED` needs `exclusion_reasons`, `NEEDS_RESEARCH` needs `missing_information`, `BLOCKED` needs `errors`.
3. Implement `parse_qualification_result(raw, account_id)` — it must never raise; on any failure it returns a `BLOCKED` result with the original error preserved.
4. Write eight contract tests minimum: one happy-path and one failing-case per invariant.

## Diagnostic (targeted fix)

The provided test suite has a gap: no test confirms `BLOCKED` results preserve the *original* raw input for debugging, not just the error message. Add that test, then check whether your implementation actually satisfies it — if it doesn't, fix `parse_qualification_result` so it does.

## Extension (optional)

Add a fifth business invariant of your own devising — for example, `rationale` must reference at least one entry in `evidence_refs` by ID. Write a failing-case test that demonstrates it catches a case the existing four invariants miss.

## Submission

- `./scripts/check.sh` output showing all contract tests passing.
- One paragraph: which of the four invariants was hardest to test correctly, and why.

## Constraints

- `qualification_agent.py` must remain byte-for-byte unchanged from Class 4 — this class is a validation layer, not a rewiring of the agent.
- No tools yet. Class 6 adds tools; `EvidenceItem` doesn't get real exercise from tool-retrieved facts until then.
- `parse_qualification_result` must never raise an unhandled exception, regardless of input — verify this with at least one deliberately malformed input in your tests.

## What "done" looks like

You can hand `parse_qualification_result` literally any dict — well-formed, malformed, or adversarial — and it always returns a valid `QualificationResult` (possibly `BLOCKED`), never a crash and never a silently accepted invalid result.
