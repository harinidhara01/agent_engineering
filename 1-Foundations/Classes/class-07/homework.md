# Class 7 Homework

## Starting checkpoint

`../class-06/golden-solution/` (or your own Class 6 submission)

## Required (30–45 minutes)

1. Build `research_tools.py`, `contracts/research_brief.py`, `research.py`, and `agents/research_agent.py`.
2. `build_research_brief` should produce a schema-valid `ResearchBrief` for all three sample accounts, with every material claim cited.
3. Get `./scripts/check.sh` passing, including the injection-attempt and conflicting-sources tests.

## Diagnostic (targeted fix)

Add a fourth mock account to `data/mock_public_sources.yaml` with two sources that disagree on a field `detect_employee_count_conflict` does **not** currently check — for example, two sources stating different industries. Confirm, by actually running your pipeline, that this conflict currently goes completely undetected and silently produces two contradictory claims sitting side by side in `claims[]`. Then decide: is that a bug worth fixing today, or a known limitation worth documenting? Either is an acceptable answer, but you must justify it in writing.

## Extension (optional)

Add a source-freshness check: a configurable threshold (e.g., 365 days) beyond which an evidence item is flagged as stale in the `ResearchBrief`, distinct from being wrong. Use the deliberately old 2023 regional-directory record for `acme-001` as your test case.

## Submission

- `./scripts/check.sh` output, all green.
- One full `ResearchBrief` JSON for `acme-001`, showing the conflict.
- Your written decision from the Diagnostic level: fix or document, and why.

## Constraints

- Research remains read-only and non-actionable. No outreach drafting yet (that's Class 8), no send action (that never exists in Book 1).
- `search_public_records` may not be extended to accept an arbitrary company name or URL — it stays scoped to known account IDs, per this checkpoint's own honest limitation.

## What "done" looks like

You can point at a specific `Conflict` object in a `ResearchBrief` and explain, from the code alone (not from memory), exactly which regular expression produced it and exactly what it would miss.
