# WidgetWare SDR Lab

A bounded agent system that researches, qualifies, and drafts outreach to prospective manufacturing and industrial-automation accounts on WidgetWare's behalf — and stops for human approval before anything leaves the building.

This checkpoint (Class 5 / `golden-solutions/class-05/`) replaces the agent's free-form prose output with a validated `QualificationResult` contract. The agent itself, its Skill, and its model call are unchanged from Class 4 — this chapter is a standalone validation layer, not a rewiring of the agent.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
./scripts/check.sh    # runs format check, lint, and tests — live-model tests skip automatically without credentials
```

## What's new this class

- `src/widgetware_sdr/contracts/evidence.py` — the `EvidenceItem` contract
- `src/widgetware_sdr/contracts/qualification.py` — the `QualificationResult` contract with four enforced business invariants, plus `parse_qualification_result()`'s fail-safe validate pipeline
- `tests/contracts/` — schema-validation and business-invariant tests, including failing-case tests for each invariant

## Repository structure

```text
widgetware-sdr/
├── README.md / SPEC.md / pyproject.toml / .env.example
├── docs/
├── config/
├── data/sample_accounts/
├── skills/
├── src/widgetware_sdr/
│   ├── contracts/
│   │   ├── evidence.py
│   │   └── qualification.py
│   ├── skills.py
│   ├── app.py
│   └── agents/qualification_agent.py   # unchanged from Class 4 — still no tools
├── tests/
│   ├── unit/
│   ├── contracts/
│   ├── integration/     # requires live credentials; skips otherwise
│   ├── scenarios/
│   └── fixtures/
└── scripts/check.sh
```

## Trying the contract pipeline

```python
from widgetware_sdr.contracts.qualification import parse_qualification_result

raw = {"account_id": "acme-001", "status": "QUALIFIED", "rationale": "Fits.", "evidence_refs": []}
result = parse_qualification_result(raw, account_id="acme-001")
print(
    result.status
)  # BLOCKED — QUALIFIED without evidence_refs is an invariant violation, not a valid result
print(result.errors)  # the validation error, preserved for debugging
```

## Known failure cases

See [`KNOWN_FAILURE_CASES.md`](KNOWN_FAILURE_CASES.md) — in particular #1: the contract exists and validates, but nothing in this checkpoint yet calls it against a real agent response.

## Completion checklist

Before treating this checkpoint as done:

- [ ] Every one of `QualificationResult`'s four business invariants (`QUALIFIED` needs evidence, `NOT_QUALIFIED` needs an exclusion, `NEEDS_RESEARCH` needs missing information, `BLOCKED` needs an error) has its own failing-case test, not just a happy-path test.
- [ ] `parse_qualification_result` never raises on malformed input — it always returns a `BLOCKED` result with the error preserved.
- [ ] The agent (`qualification_agent.py`) is byte-for-byte unchanged from Class 4 — this chapter adds a validation layer, it doesn't touch the agent.
- [ ] The agent still has no tools attached.

## Starting Class 6

1. Start from this checkpoint. Class 6 gives the agent its first real tools — three narrow, read-only functions for account, product, and ICP data — and updates its instruction to use them instead of assuming facts.
2. The `QualificationResult` and `EvidenceItem` contracts don't change structurally in Class 6, but `EvidenceItem` starts getting real exercise once tool-retrieved facts need evidence identifiers.
3. See `../../class-06/` for what Class 6 adds.

## Status

- [x] Class 1 — Project charter, and the Antigravity workspace and repository harness
- [x] Class 2 — Gemini context and instruction architecture
- [x] Class 3 — First ADK agent (embedded procedure)
- [x] Class 4 — Skills and reusable agent capabilities
- [x] Class 5 — Structured outputs and agent contracts
- [ ] Classes 6–10 — see `../../00_Course_Framework.md`
