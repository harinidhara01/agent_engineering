# Class 9 Grading Criteria

Used with `../GRADING-RUBRIC-TEMPLATE.md`. These are the criteria specific to this class — the things `pytest` cannot check, or can only check offline.

1. **The golden dataset is actually representative, not decorative.** A strong submission's cases each map to a real failure mode this course has demonstrated (conflicting evidence broke qualification in Class 7, injection attempts had to be neutralized in Class 7's research pipeline, etc.) — not ten variations on the same easy qualified/disqualified split.

2. **The release gate genuinely reports every failure, not just the first.** Feed it a system with two independent things broken at once (e.g., a business invariant violated *and* a golden-dataset case producing the wrong outcome) and confirm both appear in `reasons`. A submission that only surfaces one at a time has not met §10.5's "fails loudly" requirement.

3. **`approval_compliance_rate()`'s known limitation is stated, not hidden.** This metric only recognizes four workflow states at this checkpoint (RETRY_PENDING and NEEDS_HUMAN_REVIEW don't exist until Class 10). A strong submission's own `KNOWN_FAILURE_CASES.md` or code comment says this plainly — silently presenting the metric as complete is a real defect this class's own reference checkpoint exists to warn against.

4. **The gate's thresholds are argued, not arbitrary.** Ask the submitter to justify one threshold choice (e.g., "why does qualification accuracy need to be above X, not just non-zero?"). A strong answer connects it to a real business consequence; a weak one is "that's what seemed reasonable."

5. **Golden-dataset cases are checked into the repository as data, not generated at test time.** If a case's expected outcome is computed dynamically (e.g., by re-running the same logic the gate is supposed to check), the golden dataset isn't actually an independent, fixed source of truth.

6. **Independent understanding, not a copy.** If the submission's golden dataset, metrics, and release gate are near-identical to the gold reference in wording and structure with no evidence of independent construction, note that explicitly per the anti-gaming guidance in the generic template.
