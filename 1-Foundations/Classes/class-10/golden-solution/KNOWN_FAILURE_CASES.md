# Known Failure Cases — Class 10 Checkpoint

## Carried forward from Classes 1–6

- The semantic scenario tests in `tests/integration/` still require live credentials.
- The coordinator's scenario tests (now including the batch-loop ones) still use stub `qualify`/`review`/`draft` functions, not the real agents.
- `research.py`'s conflict detection is still one narrow regular expression.

## New at this checkpoint

### 1. `tool_calls` is a coarse proxy, not a real per-call count

`run_batch` increments `usage.tool_calls` by exactly 1 per account processed — a stand-in for actually counting each real tool invocation the workflow makes. A live deployment's Research Agent alone might make one tool call; a Qualification Agent with real tools might make three. This checkpoint's budget test (`test_stops_at_a_tool_call_budget`) genuinely confirms the *mechanism* works — the loop does stop when the counter crosses the limit — but the counter itself doesn't measure what its name claims to measure. Wiring this to the real ADK event stream (per Class 3's `app.py`, which already returns the full event list) is future work, not done here.

### 2. `LoopAgent` is deprecated in the installed ADK version

Constructing a `LoopAgent` in this checkpoint's environment (`google-adk` 2.5.0) emits: *"LoopAgent is deprecated in favor of Workflow and will be removed in a future version."* Book 1's own teaching of `LoopAgent` as the loop primitive is accurate to when the manuscript was written, but the SDK has already begun moving toward a different API (`Workflow`) that, per the same warning, doesn't yet support being used as an `LlmAgent` sub-agent — meaning there isn't yet a clean migration path even if you wanted to move off `LoopAgent` today. This is a real, live discrepancy between the book and the current SDK, not a mistake in this checkpoint's code. Treat `create_batch_loop_agent()` as correct against the book and worth revisiting against ADK's changelog before a real deployment.

### 3. The coordinator does not hard-stop on a `NOT_QUALIFIED` result

`run_workflow()` proceeds from `QUALIFYING` to `REVIEW_REQUIRED` regardless of the qualification status — it is the `review` stage's responsibility to decline `approved_for_drafting` for a disqualified account, which is what actually stops Bright Leaf Financial Advisors from reaching `AWAITING_APPROVAL` in this checkpoint's tests. This is a real design choice (the coordinator stays generic; business logic about *which* accounts deserve outreach lives in the review stage), but it means a `review` stub or a real Evidence Reviewer that fails to check qualification status would let a disqualified account through undetected by the coordinator itself.

### 4. `DEFER` is reachable in `decide()` but never actually triggered by `run_batch`

`test_decision.py` proves `decide()` returns `DEFER` when `dependency_available=False` — but nothing in `run_batch`'s actual flow ever sets that parameter to `False`; it's hardcoded to the default (`True`) in every call. The mock research source (Class 5) never fails as a genuine external dependency would — it either has data or it doesn't, and "doesn't" currently routes to `BLOCKED` (insufficient evidence), not `DEFER`. The five-way decision's `DEFER` branch is real code, tested in isolation, but currently dead code from `run_batch`'s perspective.

### 5. `AccountQueue.select_next` can let one retrying account monopolize turns

Because `select_next` always returns the *first* eligible account in list order, an account that becomes `RETRY_PENDING` sits at its original list position and will be reselected before any account later in the list gets its first attempt, if it comes earlier in the list. A large batch with one early, persistently-failing account could delay every account behind it. Book 1 §11.5 doesn't specify a fairness policy for this, and this checkpoint doesn't add one.

### 6. No test simulates an actual process restart, at either the workflow or loop level

Same gap as Class 6, now also true one layer up: `test_checkpoints_are_written_per_account` proves checkpoint files are written correctly. Nothing here kills the Python process mid-batch and restarts it against those files — `run_batch` always runs start-to-finish in one call. A genuine resume-from-checkpoint code path (reading `AccountQueue` state back from disk rather than from an in-memory object) does not exist in this checkpoint.

### 7. The golden dataset is four accounts covering ten categories

`eval/golden_dataset.py`'s ten `GoldenCase` entries reuse only four underlying accounts. `test_every_required_category_has_at_least_one_case` proves every category is *represented*, not that it's adequately *covered* — one case per category is the minimum Book 1 §10.3 asks for, not a claim of statistical confidence.
