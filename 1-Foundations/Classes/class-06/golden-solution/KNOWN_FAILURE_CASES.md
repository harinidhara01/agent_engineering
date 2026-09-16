# Known Failure Cases — Class 6 Checkpoint

## Carried forward from Classes 1–3

- The three semantic scenario tests in `tests/integration/` still require live credentials and still only prove construction offline. With tools now attached, a live run also exercises real tool-calling — untested here without credentials.
- `data/sample_accounts/` and `tests/fixtures/accounts/` remain duplicated, not shared from one source.
- Business-config drift between `config/icp.yaml` and the fixture `expected/*.yaml` files is still undetected by any test.

## New at this checkpoint

### 1. Tool tests don't cover dependency failure, permission failure, or redaction

Book 1 §7.8 lists seven things to test tools for. This checkpoint's three tools are local, read-only, and have no sensitive fields — so "dependency failure" (no external dependency exists), "permission failure" (no auth boundary exists yet), and "redaction of prohibited fields" (nothing sensitive is in this schema) are genuinely not applicable *yet*. This is not the same as "tested and passing" — it's untested because the failure mode doesn't exist in this codebase. The moment Class 5 adds a real external research source, dependency failure becomes real and needs its own test; the moment any account field becomes sensitive, redaction becomes real too.

### 2. `parse_qualification_result`'s repair step is not actually a repair

Book 1 §6.5 lists "optionally request a bounded repair for format errors" as one pipeline stage. This checkpoint's `parse_qualification_result` skips straight from "invalid" to `BLOCKED` — it never attempts to ask the model to fix a malformed response before giving up. That's a legitimate simplification for this checkpoint (fail-safe is the priority; repair is an optimization), but a submission that claims to have implemented §6.5's repair step in full would be overclaiming.

### 3. The agent's tool-calling behavior is unverified without a live run

`test_agent_has_exactly_the_three_read_tools` proves the tools are *attached*. It proves nothing about whether the model actually calls `get_account_profile` instead of assuming account facts from its own training, or whether it calls `get_icp_policy` instead of hardcoding a remembered threshold. That's exactly the kind of thing the "=== TOOLS ===" instruction section is meant to prevent, and exactly the kind of thing that can only be confirmed by inspecting a real event sequence — see `app.py`'s `run_qualification`, and run it with live credentials if you have them.

### 4. `calculate_fit_score`'s weights are arbitrary and undocumented as such

0.4 / 0.3 / 0.2 / 0.1 for industry / size / region / signal is a plausible-looking but entirely invented weighting — nothing in Book 1 specifies real weights, and this checkpoint doesn't claim otherwise, but it's worth being explicit: don't mistake this number for a calibrated score. It has never been validated against a real outcome.
