# Known Failure Cases — Class 8 Checkpoint

## Carried forward from Classes 1–5

- The semantic scenario tests in `tests/integration/` still require live credentials.
- `research.py`'s conflict detection is still one narrow regular expression.
- `calculate_fit_score`'s weights remain an invented, uncalibrated placeholder.

## New at this checkpoint

### 1. The coordinator's scenario tests use stub qualify/review/draft functions, not the real agents

`test_coordinator.py`'s five scenario tests (success, insufficient evidence, source conflict, malformed output, rejected approval) prove the **state machine, checkpointing, and partial-failure handling** are correct. They do not exercise the real `qualification_agent`, `evidence_reviewer`, or `drafting_agent` at all — those are injected as plain Python functions returning pre-built contract objects. This is a deliberate, defensible design choice (it's what makes 90 tests pass with zero API calls), but it means "the workflow works" and "the workflow works with real agents making real decisions" are two different claims, and only the first one is verified here.

### 2. "Malformed output" is simulated by an exception, not a real malformed model response

The malformed-output scenario test makes `qualify()` raise a `ValueError` directly. A real malformed response from Gemini would more likely be a `QualificationResult` that fails Pydantic validation inside `parse_qualification_result` (Class 4), which already returns `BLOCKED` rather than raising — meaning a *real* malformed-output case would never reach the coordinator's `except Exception` branch at all; it would arrive as an already-`BLOCKED` `QualificationResult` object. This checkpoint's test exercises the coordinator's own exception handling, which is a real and useful thing to test, but it is not quite the same failure path a live deployment would actually hit most often.

### 3. `run_workflow`'s conflict handling is permissive by design, and that's not obviously right

A research-brief conflict does not block the workflow — `test_source_conflict_scenario_preserves_the_conflict_through_the_run` confirms the run reaches `AWAITING_APPROVAL` even with an unresolved employee-count conflict, trusting the qualification and review stages to react to it appropriately. Whether that's the correct policy (versus routing straight to `BLOCKED` on any conflict) is a real design decision this checkpoint makes once, implicitly, and does not revisit or justify at length.

### 4. Checkpoint files are overwritten, not versioned

`_checkpoint()` writes `{account_id}.json`, replacing the previous checkpoint every time. There is no history of what the workflow's state was three stages ago beyond what's in the current `history` list — if you needed to debug exactly when a specific field changed, the checkpoint file alone won't tell you; you'd need the coordinator's own logs.

### 5. No test actually simulates a process restart

"Resume from checkpoint" is described in the Hands-on Lab and supported by `load_checkpoint()`, but no test in this checkpoint kills a running process and restarts it against a saved checkpoint — the checkpoint read/write round-trip is tested, but not an actual resume-and-continue flow, because `run_workflow` always runs a account from `RECEIVED` to completion in one call; there's no code path yet that starts from a loaded mid-run checkpoint instead of from the beginning. That capability doesn't exist until Class 7's loop.
