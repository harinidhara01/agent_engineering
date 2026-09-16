# Skill: Evidence Classification

## Identity

- Name: evidence_classification
- Version: 1.0.0
- Owner: WidgetWare SDR Lab course
- Purpose: Label a piece of supplied information as verified fact, derived fact, inference, unknown, or conflict — WidgetWare's evidence policy (Book 1 §3.5), applied consistently by any agent that needs it.

## Inputs

- One or more statements or pieces of information, each with a source.

## Procedure

1. Verified fact — the statement is directly stated by an approved source, with no interpretation required.
2. Derived fact — the statement is deterministically calculated from verified facts (e.g., "over the minimum" derived from a stated employee count and the ICP threshold).
3. Inference — the statement is a reasoned conclusion that goes beyond what any source directly states, and remains uncertain.
4. Unknown — no source addresses the statement at all.
5. Conflict — two or more credible sources disagree, and the disagreement itself must be surfaced, not silently resolved.

## Quality criteria

- Never present an inference using the same confident wording as a verified fact.
- A conflict is never resolved by picking the more convenient value without saying so.
- "Unknown" is a valid, expected output — not a failure to be avoided by guessing.

## Examples

- "The company has 22,000 employees" (stated directly in the account profile) → **verified fact**.
- "This company is large" (derived from the 22,000 figure and a stated size threshold) → **derived fact**.
- "This company likely has a slow-moving IT department" (not stated anywhere, reasoned from company size alone) → **inference**.
- "The company's current ERP vendor" (not mentioned in any supplied source) → **unknown**.
- "One source says 22,000 employees; another says 18,000" → **conflict**, both values and both sources should be surfaced.
