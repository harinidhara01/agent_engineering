# Building Class 5 with Antigravity

Goal: a validated `QualificationResult` contract that turns the agent's free-form prose into a machine-checkable result, without touching the agent itself. `golden-solution/` in this folder is the reference. Build your own copy in `my-work/gemini-book-1/class-05/`, then diff.

## Prerequisites

- **`../SETUP.md` complete.** This class is fully offline — no model credentials needed, since nothing here calls Gemini directly.
- Your Class 4 checkpoint, passing `./scripts/check.sh`.

## Steps

1. Write `src/widgetware_sdr/contracts/evidence.py` yourself: an `EvidenceItem` Pydantic v2 model (`extra="forbid"`) capturing at minimum a source, a claim, and a category distinguishing verified fact from inference — reusing Class 2's evidence vocabulary.

2. Ask Antigravity for the qualification contract, but be explicit about the invariants — this is the part a generic prompt will miss:

   > "Write `src/widgetware_sdr/contracts/qualification.py`. Define `QualificationResult` as a Pydantic v2 model (`extra='forbid'`) with fields for `account_id`, `status` (an enum: QUALIFIED, NOT_QUALIFIED, NEEDS_RESEARCH, BLOCKED), `rationale`, `evidence_refs`, `exclusion_reasons`, `missing_information`, and `errors`. Add a `@model_validator(mode='after')` enforcing: QUALIFIED requires non-empty `evidence_refs`; NOT_QUALIFIED requires non-empty `exclusion_reasons`; NEEDS_RESEARCH requires non-empty `missing_information`; BLOCKED requires non-empty `errors`."

3. Write `parse_qualification_result(raw: dict, account_id: str) -> QualificationResult` yourself, by hand — this fail-safe wrapper is the part worth understanding line by line, not delegating: try to construct `QualificationResult(**raw)`; on any `ValidationError` (schema or invariant), catch it and return a `BLOCKED` result whose `errors` field preserves the original exception message and whose other fields are safely empty/default.

4. Write the contract tests: one happy-path test per status value (four total), one failing-case test per invariant (four total, each deliberately violating one invariant), and at least one test feeding `parse_qualification_result` a completely malformed dict (wrong types, missing required keys) confirming it returns `BLOCKED` and never raises.

5. Confirm `qualification_agent.py` is untouched — diff it against your Class 4 checkpoint and verify zero changes.

## Verify

```
cd my-work/gemini-book-1/class-05
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
./scripts/check.sh
```

Expect all contract tests and prior offline tests to pass; integration tests skip (without credentials) or pass (with them) exactly as in Class 4, since the agent itself hasn't changed.

## Compare against the reference

`golden-solution/tests/contracts/` is the reference for what a complete invariant test suite looks like — pay attention to how each failing-case test constructs a minimally-invalid object (right status, missing the one required field) rather than an object that's wrong in several ways at once, which would make it unclear which invariant actually caught it.

## Grade it

Passing tests doesn't prove the invariants match the actual business rules, or that the fail-safe pipeline handles every realistic malformed-input shape. Run the quality check: `GRADING.md` in this folder plus `../GRADING-RUBRIC-TEMPLATE.md`.
