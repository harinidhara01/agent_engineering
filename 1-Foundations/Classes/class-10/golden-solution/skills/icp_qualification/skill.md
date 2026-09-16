# Skill: WidgetWare ICP Qualification

## Identity

- Name: icp_qualification
- Version: 1.0.0
- Owner: WidgetWare SDR Lab course
- Purpose: Decide whether a target account fits WidgetWare's ideal customer profile, using only supplied account data.

## Inputs

- A normalized account profile (industry, employee count, region, known challenges, source notes).
- The current ICP configuration (minimum employee count, preferred/excluded industries, preferred regions, buying signals).
- Any available evidence (source notes, prior research).

## Procedure

1. Check explicit exclusion criteria first. If the account's industry is in the excluded-industries list, the outcome is `DO_NOT_QUALIFY` regardless of any other positive signal.
2. Compare the account's attributes against the ICP thresholds: employee count against the minimum, industry against the preferred list, region against the preferred list.
3. Identify confirmed pain signals in the account's known challenges and source notes — concrete, specific statements, not vague mentions.
4. Identify what information is missing that would be needed to qualify or disqualify confidently.
5. Distinguish fact (directly stated) from inference (your own reasoning about what a fact implies). Never state an inference with the confidence of a fact.
6. Select a provisional outcome:
   - `QUALIFY` — meets the ICP thresholds and shows a concrete pain signal.
   - `DO_NOT_QUALIFY` — fails an explicit exclusion or clearly falls outside the thresholds.
   - `NEEDS_RESEARCH` — a decisive fact (most commonly employee count) is missing, or the available signal is too vague to be decisive either way.
7. Explain the outcome: which specific criteria were matched or failed, which evidence supports the pain signal (if any), and what remains unknown.

## Quality criteria

- No fabricated account attributes — never state an employee count, industry, or fact that was not supplied.
- All decisive claims trace to input evidence.
- Exclusions override positive heuristics — an excluded industry is `DO_NOT_QUALIFY` even with a strong pain signal.
- Insufficient evidence produces `NEEDS_RESEARCH`, never a guess.
- Rationale is concise and actionable — a real SDR should be able to act on it without asking a follow-up question.

## Examples

See `examples/qualified.md`, `examples/unqualified.md`, and `examples/needs_research.md`.
