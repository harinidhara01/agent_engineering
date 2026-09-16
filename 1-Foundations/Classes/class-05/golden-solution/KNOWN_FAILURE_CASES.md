# Known Failure Cases — Class 5 Checkpoint

## Carried forward from Classes 1–4

- The semantic scenario tests in `tests/integration/` still require live credentials and still only prove agent construction offline.
- `data/sample_accounts/` and `tests/fixtures/accounts/` remain duplicated, not shared from one source.

## New at this checkpoint

### 1. The contracts exist, but nothing in this checkpoint actually produces one from the agent yet

`QualificationResult` and `EvidenceItem` are fully defined and tested in isolation — schema validation and the four business invariants all pass. But `qualification_agent.py` is completely unchanged from Class 4: it still returns free-form prose, and nothing in this checkpoint calls `parse_qualification_result()` on a real agent response. Per Book 1 §6's own Hands-on Lab, this is the intended scope for this chapter (contracts as a standalone deliverable) — the wiring that actually makes the agent's output conform happens implicitly as later chapters build on top of this contract, not as an explicit step in this one.

### 2. `parse_qualification_result`'s repair step is not actually a repair

Book 1 §6.5 lists "optionally request a bounded repair for format errors" as one pipeline stage. This checkpoint's `parse_qualification_result` skips straight from "invalid" to `BLOCKED` — it never attempts to ask the model to fix a malformed response before giving up. A legitimate simplification (fail-safe first, repair is an optimization), but worth being explicit about if you're comparing this checkpoint against the book's full description.

### 3. Business-config drift still isn't caught by anything

`config/icp.yaml` and `docs/widgetware-business-brief.md` must still agree by hand — nothing here fails loudly if they diverge.
