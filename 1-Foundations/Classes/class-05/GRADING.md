# Class 5 Grading Criteria

Used with `../GRADING-RUBRIC-TEMPLATE.md`. These are the criteria specific to this class — the things `pytest` cannot check, or can only check offline.

1. **The invariants encode real business rules, not arbitrary type constraints.** A strong submission can explain, in one sentence per invariant, what real-world mistake it prevents (e.g., "a rep can't say QUALIFIED and then not point at why" for the evidence_refs rule). If a submission can't explain the "why" behind an invariant, it likely copied it without understanding it.

2. **`parse_qualification_result` genuinely never raises.** Grep for any bare `QualificationResult(**raw)` call outside a `try`/`except`, or any place a caller could get an unhandled `ValidationError`. The entire point of this class is that malformed input becomes a `BLOCKED` result, not a crash.

3. **The failing-case tests are minimally invalid, not incidentally invalid.** A strong failing-case test for the `QUALIFIED`-needs-evidence invariant sets `status=QUALIFIED` and an empty `evidence_refs`, with every other field otherwise valid — not a test that's also missing `account_id` or has a malformed `rationale`, which would make it unclear which check actually failed.

4. **The `BLOCKED` error is actually useful, not just present.** Check that `errors` contains information a person could act on (which field, which rule, what value) — not a generic string like `"validation failed"` that's technically non-empty but useless for debugging.

5. **The agent is verifiably untouched.** A submission should be able to show (via `git diff` or a direct file comparison) that `qualification_agent.py` has zero changes from its Class 4 state. If it changed, ask why — the answer should never be "to make the contract layer work."

6. **Independent understanding, not a copy.** If the submission's `qualification.py` and its tests are near-identical to the gold reference in wording and structure with no evidence of independent construction, note that explicitly per the anti-gaming guidance in the generic template.
