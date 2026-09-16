# Class 5 Kahoot — 8 Questions

Run during 0:45–0:55. Correct answer marked with **✓**.

---

**1. (Terminology)** What is the difference between a schema and a business invariant (§6.3–6.4)?
- A) They're interchangeable terms for the same thing
- **✓** B) A schema checks shape and types; a business invariant checks domain-specific rules a valid-shaped object can still violate
- C) A schema is written in Python; a business invariant is written in YAML
- D) Business invariants only apply to numeric fields

**2. (Terminology)** What does "fail-safe" mean for a parsing pipeline (§6.5), and how is it different from "fail-fast"?
- **✓** A) Fail-safe returns a well-formed error result (`BLOCKED`) instead of crashing; fail-fast raises immediately on the first problem
- B) They're the same design pattern with different names
- C) Fail-safe means the pipeline retries automatically until it succeeds
- D) Fail-fast means errors are logged but otherwise ignored

**3. (Architecture)** Why does `QUALIFIED` require `evidence_refs` to be non-empty as a business rule, not just a type check?
- **✓** A) A list can be present and correctly typed while still being empty — the business rule is that a qualified claim needs actual supporting evidence, which a type check alone can't enforce
- B) Pydantic doesn't support empty-list validation at all
- C) It's arbitrary — any status could require any field
- D) Evidence is only needed for `NOT_QUALIFIED` results

**4. (Architecture)** What does `parse_qualification_result()` return when given malformed input, and why is that the right answer?
- **✓** A) A `BLOCKED` result with the original error preserved — never an unhandled exception, and never a silently "successful" invalid result
- B) `None`, so callers must remember to check for it
- C) It raises `ValueError` immediately
- D) It retries with a corrected version of the input

**5. (Failure analysis)** A qualification result claims `NOT_QUALIFIED` but has an empty `exclusion_reasons` list — what should happen?
- **✓** A) The `model_validator` rejects it, and `parse_qualification_result` converts that into a `BLOCKED` result with the error preserved
- B) It should pass — exclusion reasons are optional documentation, not a requirement
- C) It should silently default to `QUALIFIED` instead
- D) It should raise an unhandled exception that crashes the caller

**6. (Security/governance)** Why is preserving the original error on a `BLOCKED` result more useful than just discarding bad input silently?
- **✓** A) It gives a human or downstream system enough information to actually diagnose and fix the source of the bad input, instead of just knowing something failed
- B) It has no practical benefit — it's just convention
- C) It's required by Pydantic's API and can't be turned off
- D) It makes the pipeline run faster

**7. (WidgetWare scenario)** The agent's prose rephrases itself between calls but its meaning is the same. How does the contract layer stay stable regardless?
- **✓** A) The contract only cares about the parsed, structured fields (`status`, `evidence_refs`, etc.) — not the exact wording the agent used to arrive at them
- B) It doesn't — any rephrasing breaks the contract layer
- C) The contract re-runs the agent until the wording matches exactly
- D) The contract ignores the agent's output entirely

**8. (Connecting back)** How do Class 2's evidence-policy categories (fact vs. inference) show up as fields inside `EvidenceItem`?
- **✓** A) `EvidenceItem` carries a typed field distinguishing verified fact from inference, directly reflecting the vocabulary Class 2 established for evidence handling
- B) They don't — evidence categorization was dropped after Class 2
- C) `EvidenceItem` replaces Class 2's vocabulary with a new, unrelated one
- D) Fact vs. inference only matters once Class 7's research pipeline exists

---

## Facilitator notes

- Question 4 is the crux of the whole class — "never raise, never silently pass" is the fail-safe principle participants will apply again in Class 7's research pipeline and Class 8's workflow state machine.
- Question 7 is worth a live demo if time allows: run the agent twice on the same account, show the prose differs slightly, then show the parsed `QualificationResult` is identical in the fields that matter.
