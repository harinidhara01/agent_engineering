# Known Failure Cases — Class 7 Checkpoint

## Carried forward from Classes 1–4

- The semantic scenario tests in `tests/integration/` still require live credentials and still only prove construction offline.
- `data/sample_accounts/` and `tests/fixtures/accounts/` remain duplicated, not shared from one source.
- `calculate_fit_score`'s weights are still an invented, uncalibrated placeholder.

## New at this checkpoint

### 1. The research source is a local mock, not a real external source

`search_public_records` reads `data/mock_public_sources.yaml` — a small, hand-authored, deterministic file, not a real web search, news API, or MCP server. This is a genuine simplification, not just a testing convenience: it means Book 1 §8.3's "assess source quality and freshness" guidance is only exercised against sources this course invented and dated for the purpose, never a genuinely unpredictable real-world source. A real integration (a live MCP server, an actual search API) would need its own error handling, rate limiting, and result-quality variance this mock never exhibits.

### 2. Conflict detection is a single regular expression, not a general capability

`detect_employee_count_conflict` only catches the specific phrase pattern "approximately N employees" appearing more than once with different values. It would not catch a conflict phrased differently ("roughly 22K staff" vs. "approximately 19,500 employees"), a conflict in a different field entirely (industry classification, headquarters location), or a conflict spread across more than two sources with partial agreement. Book 1 §8.4 does not specify a general algorithm either — but a reader could easily overestimate what this checkpoint's conflict detection actually covers if they don't read the regex directly.

### 3. The Research Agent's isolation instruction is untested against a real model

Exactly the same caveat as Class 3 and Class 4: `test_instruction_establishes_retrieved_content_as_untrusted` proves the instruction *says* the right thing. It proves nothing about whether Gemini actually resists the embedded "IGNORE ALL PREVIOUS INSTRUCTIONS" text in `meridian-003`'s mock evidence when asked to synthesize a brief. That test requires live credentials and lives in `tests/integration/` — not yet written for the Research Agent specifically at this checkpoint; see the Extension homework.

### 4. `research.py`'s claim construction is naive: one claim per evidence item, verbatim

Real research synthesis would combine, compare, and selectively cite evidence, not turn every non-conflicting record into a claim with identical wording. This checkpoint's deterministic pipeline is intentionally simple so it can be fully tested offline — the Research Agent (`research_agent.py`) is where actual synthesis is meant to happen, and that part is exactly what requires a live model to evaluate.

### 5. Freshness is recorded but never enforced

`EvidenceItem.retrieved_at` is populated for every item, and the Research Agent's instruction tells the model to flag sources over a year old — but nothing in the deterministic pipeline itself computes an item's age or blocks a stale item from becoming a claim. A stale claim (like the 2023 employee-count record) still becomes ordinary claim text unless it happens to also be part of a detected conflict.
