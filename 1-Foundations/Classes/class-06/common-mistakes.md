# Class 6 — Common Mistakes to Discuss (0:00–0:20)

Reviewing Class 5's homework before revealing `golden-solution/`.

## In the required build (contract invariants)

- **Invariants tested only on the happy path.** A submission with a passing test for each valid status but no test proving the *invalid* case is actually rejected hasn't proven the invariant exists — it's proven the valid case is valid, which was never in doubt.

## In the extension (fifth business invariant)

- **A `BLOCKED` error that's technically non-empty but not actually useful.** A generic string like `"validation failed"` satisfies the type check but gives a reviewer nothing to act on — a strong error names the field, the rule, and the offending value.

## Talking points to set up today's class

- Ask: "Every fact in a `QualificationResult` right now — the employee count, the industry — where did the agent actually get it from?" The expected answer, once people think it through, is "wherever the caller happened to put it in the per-call message" — the agent has never gone and looked anything up itself.
- Preview least privilege before revealing it: ask what the damage ceiling should be if one of today's tools were compromised. Most will correctly guess "small, because it's read-only" — that's the design goal made explicit.

## Golden solution reveal

Run Class 5's agent live, print a valid `QualificationResult`, and ask the room to trace one `evidence_refs` entry back to its source. There isn't one — it's just whatever was in the per-call message. Then ask: "What would it take for the agent to go verify this itself?" That's the whole gap this class closes.
