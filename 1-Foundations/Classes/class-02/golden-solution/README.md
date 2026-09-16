# WidgetWare SDR Lab

A bounded agent system that researches, qualifies, and drafts outreach to prospective manufacturing and industrial-automation accounts on WidgetWare's behalf — and stops for human approval before anything leaves the building.

This checkpoint (Class 2 / `golden-solutions/class-02/`) adds a deliberate model and context architecture on top of Class 1's workspace: system instructions, business configuration as data, and a context-assembly pipeline that keeps account-supplied content structurally isolated from system policy. No ADK agent exists yet — there is still no model call anywhere in this codebase.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env  # fill in any local values; never commit .env
./scripts/check.sh    # runs format check, lint, and tests in one command
```

## What's new this class

- `config/products.yaml`, `config/icp.yaml`, `config/policies.yaml` — WidgetWare's stable business rules, as data
- `src/widgetware_sdr/instructions.py` — fixed system instructions and centralized model selection
- `src/widgetware_sdr/context_builder.py` — assembles system instructions, business context, task context, and evidence into one `ContextPackage`, with account-supplied content always confined to a clearly delimited, labeled evidence section
- `tests/unit/test_context_builder.py` — five tests: required policy language present, a clearly qualified account, a clearly unqualified account, an account with insufficient evidence, and a malicious note that cannot override system instructions

## Repository structure

```text
widgetware-sdr/
├── README.md
├── SPEC.md
├── pyproject.toml
├── .env.example
├── docs/
│   ├── widgetware-business-brief.md
│   └── acceptance-criteria.md
├── config/
│   ├── products.yaml
│   ├── icp.yaml
│   └── policies.yaml
├── src/
│   └── widgetware_sdr/
│       ├── __init__.py
│       ├── health.py
│       ├── instructions.py
│       └── context_builder.py
├── tests/
│   ├── unit/
│   ├── contracts/      # populated starting Class 4
│   ├── scenarios/
│   └── fixtures/
│       ├── accounts/
│       └── expected/
└── scripts/
    └── check.sh
```

## Sample inputs and expected outputs

`tests/fixtures/accounts/*.yaml` and `tests/fixtures/expected/*.yaml` are no longer just carried forward — `test_context_builder.py` now loads the three scenario accounts directly from `accounts/` and asserts against the `icp_match` section of `expected/`, instead of hardcoding account data inline in the test. This is the first checkpoint where the fixture files are actually load-bearing, not just documentation.

`icp_match` deliberately encodes "unknown" (`null`) separately from "fails the criterion" (`false`) for Meridian's employee count — see `KNOWN_FAILURE_CASES.md` #2 for why that distinction matters.

## Known failure cases

See [`KNOWN_FAILURE_CASES.md`](KNOWN_FAILURE_CASES.md).

## Completion checklist

Before treating this checkpoint as done:

- [ ] `config/icp.yaml`, `config/products.yaml`, `config/policies.yaml` match `docs/widgetware-business-brief.md` exactly — no drift between the two.
- [ ] `instructions.py`'s `SYSTEM_INSTRUCTIONS` is a fixed constant with no account-derived content anywhere in it.
- [ ] `context_builder.py` has no model call anywhere in it — verify with `grep -ri "generate_content\|gemini\|adk" src/widgetware_sdr/context_builder.py` and confirm no real hits.
- [ ] All five tests in `test_context_builder.py` pass, and the malicious-note test specifically asserts on section *ordering*, not just text presence.
- [ ] You have printed `context.assembled_prompt` at least once for a real scenario and read it end to end.

## Starting Class 3

1. Start from this checkpoint. Class 3 adds the first real ADK `Agent` and its first real Gemini model call — everything built so far (`context_builder.py`, `instructions.py`, the fixtures) becomes the input to that agent, unchanged.
2. The malicious-note test's guarantee is about to be tested for real. Class 3 is the first checkpoint where you can actually observe whether a live Gemini call, given this exact assembled context, behaves the way the structural isolation intends.
3. See `../../class-03/` for what Class 3 adds.

## Status

- [x] Class 1 — Project charter, and the Antigravity workspace and repository harness
- [x] Class 2 — Gemini context and instruction architecture
- [ ] Classes 3–10 — see `../../00_Course_Framework.md`
