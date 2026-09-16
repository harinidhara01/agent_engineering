# WidgetWare SDR Lab

A bounded agent system that researches, qualifies, and drafts outreach to prospective manufacturing and industrial-automation accounts on WidgetWare's behalf — and stops for human approval before anything leaves the building.

This checkpoint (Class 9 / `golden-solutions/class-09/`) proves the Class 8 workflow is good enough to ship: a golden dataset covering all ten required categories, deterministic metrics, and a release gate that fails loudly and names every unmet condition. No loop yet — that's Class 10, deliberately after this one.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
./scripts/check.sh
```

## What's new this class

- `eval/golden_dataset.py` — 10 cases covering every required category (§10.3)
- `eval/metrics.py` — deterministic metrics: contract validity, evidence coverage, prohibited-action scan of the actual source tree
- `eval/release_gate.py` — the seven §10.8 conditions as one executable, testable function
- `eval/observability.py` — a structured event recorder answering "why did this case end in X?"

## Repository structure

```text
widgetware-sdr/
├── src/widgetware_sdr/
│   ├── eval/
│   │   ├── golden_dataset.py / metrics.py / release_gate.py / observability.py
│   └── workflow/    # unchanged from Class 8 — still 10 states, no loop states yet
├── tests/
│   ├── unit/ / contracts/ / tools/ / research/ / workflow/ / eval/
│   └── integration/       # requires live credentials; skips otherwise
└── scripts/check.sh
```

## Trying the release gate

```python
from widgetware_sdr.eval.release_gate import check_release_gate
from widgetware_sdr.eval.metrics import prohibited_action_rate

result = check_release_gate(
    all_unit_and_contract_tests_pass=True,
    scenario_pass_rate=0.97,
    prohibited_action_count=prohibited_action_rate(),
    evidence_coverage_rate=1.0,
    known_limitations_documented=True,
    deployment_identity_is_least_privilege=True,
    rollback_instructions_exist=True,
)
print(result.passed, result.reasons)
```

## Known failure cases

See [`KNOWN_FAILURE_CASES.md`](KNOWN_FAILURE_CASES.md) — in particular #2: `approval_compliance_rate` will need updating once Class 10 adds two more workflow states.

## Completion checklist

Before treating this checkpoint as done:

- [ ] All ten required golden-dataset categories are represented — verified, not assumed.
- [ ] `check_release_gate` fails loudly when any of its seven conditions isn't met, and reports every failing condition, not just the first.
- [ ] `prohibited_action_rate()` returns 0.0 against this checkpoint's actual source tree.
- [ ] The five-case final demonstration (success, insufficient-evidence, conflict, safety, approval-rejected) can be delivered live using the Class 8 workflow, unchanged.

## Starting Class 10

1. Start from this checkpoint. Class 10 takes this exact, evaluated workflow and wraps it — unchanged — in a bounded ADK loop that processes a queue of accounts unattended.
2. `approval_compliance_rate` (see `KNOWN_FAILURE_CASES.md` #2) will need its compliant-states set extended once the loop adds `RETRY_PENDING` and `NEEDS_HUMAN_REVIEW`.
3. See `../../class-10/` for what Class 10 adds.

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
- [ ] Class 10 — see `../../00_Course_Framework.md`
