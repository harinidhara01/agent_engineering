# Class 5 — Structured Outputs and Agent Contracts

**Manuscript source:** Book 1, Chapter 6 — Structured Outputs and Agent Contracts
**Seven-Step mapping:** Primary: Evaluate & Govern / Supporting: Design Agent Capabilities, Build the Harness
**Golden solution produced:** `class-05/golden-solution/`
**Starting checkpoint:** `class-04/golden-solution/`

## 0:00–0:20 — Homework review, common mistakes, golden solution reveal

- **Review homework:** ask participants to show their independent Skill consumer script, and confirm it loads `icp_qualification` without touching `qualification_agent.py`.
- **Common mistakes to flag:** Skill procedures that read well but never actually got tested against the boundary case; Evidence Classification examples with no genuinely ambiguous case.
- **Golden solution reveal:** run Class 4's agent live, print its raw prose response, then ask: "If I asked your production system to route on this response's outcome right now, in code — how would you do it?" (Answer: string matching against prose that might rephrase itself any call. That's the problem today solves.)

## Slide outline (0:20–0:45)

1. Current WidgetWare state: an agent that reasons well but returns free-form prose
2. Today's dependency: Class 4's Skill-driven agent doesn't change — only what happens to its output
3. Business objective: a validated, machine-checkable qualification result, safe to route on
4. Core concept: why prose isn't enough (§6.1–6.2) — a downstream system can't safely branch on "it looks qualified"
5. Terminology: schema vs. contract vs. validation (§6.3) — a schema describes shape; a contract adds business invariants; validation enforces both
6. Architecture: `QualificationResult`'s four business invariants (§6.4) — QUALIFIED needs evidence, NOT_QUALIFIED needs exclusions, NEEDS_RESEARCH needs missing info, BLOCKED needs an error
7. Seven Steps mapping: Evaluate & Govern — the first chapter squarely about making an agent's output trustworthy
8. Gemini vs. deterministic code: the agent still reasons in prose; parsing, schema validation, and invariant checks are pure deterministic code
9. Security: fail-safe design (§6.5) — malformed output becomes a `BLOCKED` result with the error preserved, never a silent pass-through
10. Today's increment: `contracts/evidence.py`, `contracts/qualification.py`, `parse_qualification_result()`
11. Lab architecture: one failing-case test per invariant — four ways to be wrong, one way to be right
12. Acceptance criteria: the agent itself is byte-for-byte unchanged — this is a validation layer, not a rewiring

## Kahoot (8 questions)

- Terminology: What is the difference between a schema and a business invariant (§6.3–6.4)?
- Terminology: What does "fail-safe" mean for a parsing pipeline (§6.5), and how is it different from "fail-fast"?
- Architecture: Why does `QUALIFIED` require `evidence_refs` to be non-empty as a business rule, not just a type check?
- Architecture: What does `parse_qualification_result()` return when given malformed input, and why is that the right answer?
- Failure analysis: A qualification result claims `NOT_QUALIFIED` but has an empty `exclusion_reasons` list — what should happen?
- Security/governance: Why is preserving the original error on a `BLOCKED` result more useful than just discarding bad input silently?
- WidgetWare scenario: The agent's prose rephrases itself between calls but its meaning is the same — how does the contract layer stay stable regardless?
- Connecting back: How do Class 2's evidence-policy categories (fact vs. inference) show up as fields inside `EvidenceItem`?

## Build together (0:55–1:35)

- `contracts/evidence.py` — `EvidenceItem` (Pydantic v2, `extra="forbid"`)
- `contracts/qualification.py` — `QualificationResult` with `@model_validator(mode="after")` enforcing all four invariants
- `parse_qualification_result(raw, account_id)` — the fail-safe pipeline: parse, validate, on any failure return `BLOCKED` with the error preserved, never raise

## Test and diagnose (1:35–1:50)

1. Run the four happy-path tests: one per status value, each with valid supporting fields.
2. Run the four failing-case tests: one per invariant, each deliberately violating it.
3. Feed `parse_qualification_result` a completely malformed dict (wrong types, missing fields) — confirm it returns `BLOCKED`, never raises.
4. Diagnose: is a failure in the schema (wrong type) or the business invariant (right type, wrong business logic)?
5. Apply the smallest fix — usually one `model_validator` condition, not a schema redesign.
6. Re-run the full contract test suite.

## Homework

| Level | Task |
| ----- | ---- |
| **Required** | `QualificationResult` and `EvidenceItem` contracts built and passing all eight contract tests (four happy-path, four failing-case) |
| **Diagnostic** | The provided `parse_qualification_result` test suite has a gap: no test confirms `BLOCKED` results preserve the *original* raw input for debugging, not just the error message. Add that test, then confirm the implementation actually satisfies it |
| **Extension** | Add a fifth business invariant of your own devising (e.g., `rationale` must reference at least one `evidence_refs` entry by ID) and demonstrate it catches a case the existing four miss |

- **Starting checkpoint:** `class-04/golden-solution/`
- **Files participants may modify:** `src/widgetware_sdr/contracts/`, `tests/contracts/`
- **Expected behavior:** malformed or invariant-violating input never crashes the pipeline — it always yields a `BLOCKED` result with the error preserved
- **Tests that must pass:** all contract tests, both happy-path and failing-case
- **Submission:** test output showing all eight (or more) contract tests passing
- **Constraints:** the agent itself (`qualification_agent.py`) must remain byte-for-byte unchanged from Class 4 — no tools yet (Chapter 7)

## Golden solution: `class-05/`

Adds the contracts layer on top of `class-04/` without touching the agent. README explicitly notes: "The agent itself, its Skill, and its model call are unchanged from Class 4 — this chapter is a standalone validation layer, not a rewiring of the agent."

## Bridge to Class 6

Class 6 gives the agent its first real tools — three narrow, read-only functions for account, product, and ICP data. The `QualificationResult` and `EvidenceItem` contracts don't change structurally, but `EvidenceItem` starts getting real exercise once tool-retrieved facts need evidence identifiers.
