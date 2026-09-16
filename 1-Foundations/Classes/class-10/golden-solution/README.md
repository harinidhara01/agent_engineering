# WidgetWare SDR Lab

A bounded agent system that researches, qualifies, and drafts outreach to prospective manufacturing and industrial-automation accounts on WidgetWare's behalf — and stops for human approval before anything leaves the building.

This checkpoint (Class 10 / `golden-solutions/class-10/`) closes Book 1: a bounded ADK loop that wraps the unchanged Class 8 workflow to process a queue of accounts unattended, stopping for a reason it can name. It builds directly on Class 9's evaluation harness and release gate — this chapter only automates what Class 9 already proved was good enough to ship.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
./scripts/check.sh
```

## What's new this class

- `workflow/state_machine.py` extended with `RETRY_PENDING` and `NEEDS_HUMAN_REVIEW` (now 12 states total)
- `loop/budget.py`, `loop/decision.py` — the five-way decision (CONTINUE/RETRY/STOP/DEFER/ESCALATE)
- `loop/account_queue.py` — work selection that never reprocesses a settled account
- `loop/run_report.py` — every run names a stop reason
- `loop/batch_runner.py` — `run_batch()` (fully offline-testable) and `create_batch_loop_agent()` (the real ADK `LoopAgent` wiring — see `KNOWN_FAILURE_CASES.md` #2 for a live SDK deprecation warning worth knowing about)
- `eval/metrics.py`'s `approval_compliance_rate()` updated to recognize the two new loop states as compliant

## Repository structure

```text
widgetware-sdr/
├── src/widgetware_sdr/
│   ├── eval/
│   │   ├── golden_dataset.py / metrics.py / release_gate.py / observability.py
│   ├── loop/
│   │   ├── budget.py / decision.py / account_queue.py / run_report.py / batch_runner.py
│   └── workflow/state_machine.py   # now 12 states
├── tests/
│   ├── unit/ / contracts/ / tools/ / research/ / workflow/ / eval/ / loop/
│   └── integration/       # requires live credentials; skips otherwise
└── scripts/check.sh
```

## Trying the batch loop

```python
from widgetware_sdr.loop.account_queue import AccountQueue, QueuedAccount
from widgetware_sdr.loop.batch_runner import run_batch
from widgetware_sdr.loop.budget import Budget

queue = AccountQueue(accounts=[QueuedAccount("acme-001"), QueuedAccount("brightleaf-002")])
budget = Budget(
    max_accounts_per_run=10,
    max_attempts_per_account=2,
    max_wall_clock_seconds=30.0,
    max_tool_calls=1000,
    max_consecutive_failures=5,
)

report = run_batch(queue, qualify=..., review=..., draft=..., budget=budget)
print(report.stop_reason, report.status_totals)
```

## Known failure cases

See [`KNOWN_FAILURE_CASES.md`](KNOWN_FAILURE_CASES.md) — in particular #1 (tool-call budget is a coarse proxy) and #2 (a real, live `LoopAgent` deprecation warning in the current ADK version).

## Completion checklist

Before treating this checkpoint as done:

- [ ] `run_batch` never reprocesses a settled account — verified by actually running the batch twice against the same queue.
- [ ] A recoverable failure retries up to (and not beyond) `max_attempts_per_account`, then escalates to `NEEDS_HUMAN_REVIEW`.
- [ ] The loop stops at every budget it declares, not only the account limit — verified by a dedicated test per budget dimension.
- [ ] `SENT` still does not exist as a state, even after adding `RETRY_PENDING` and `NEEDS_HUMAN_REVIEW`.
- [ ] `eval/metrics.py`'s `approval_compliance_rate()` recognizes the two new loop states — this was a known gap in Class 9, closed here.

## Book 1 is complete

WidgetWare SDR Lab now researches, qualifies, reviews, and drafts outreach for one account on request, or for a bounded queue of accounts unattended — evaluated, release-gated, and unable to send anything externally, structurally, at every layer built across these ten classes.

Book 2 continues the same system into enterprise-platform territory — memory, enterprise retrieval, adaptive planning, distributed agent collaboration, identity, governance, and continuous evaluation — as its own ten-class program, starting from this checkpoint.

## Status

- [x] Class 1 — Project charter, and the Antigravity workspace and repository harness
- [x] Class 2 — Gemini context and instruction architecture
- [x] Class 3 — First ADK agent (embedded procedure)
- [x] Class 4 — Skills and reusable agent capabilities
- [x] Class 5 — Structured outputs and agent contracts
- [x] Class 6 — Tool engineering
- [x] Class 7 — MCP and evidence-backed research
- [x] Class 8 — Multi-agent workflow and human approval
- [x] Class 9 — Evaluate, deploy, and demonstrate
- [x] Class 10 — Loop engineering with ADK
