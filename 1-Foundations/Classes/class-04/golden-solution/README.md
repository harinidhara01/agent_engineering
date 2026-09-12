# WidgetWare SDR Lab

A bounded agent system that researches, qualifies, and drafts outreach to prospective manufacturing and industrial-automation accounts on WidgetWare's behalf — and stops for human approval before anything leaves the building.

This checkpoint (Class 4 / `golden-solutions/class-04/`) extracts the qualification procedure out of the agent's embedded instruction (Class 3) and into a reusable Skill. The agent's boundary and model call are unchanged from Class 3 — only where its reasoning procedure lives has changed.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env  # fill in GOOGLE_API_KEY (or GOOGLE_CLOUD_PROJECT) to run the agent for real
./scripts/check.sh    # runs format check, lint, and tests — live-model tests skip automatically without credentials
```

## What's new this class

- `skills/icp_qualification/` — the qualification procedure, extracted from Class 3's embedded string: `skill.md`, three worked examples, and `tests/cases.yaml` (semantic evaluation cases, distinct from the deterministic unit tests)
- `skills/evidence_classification/` — a lightweight new Skill labeling information as verified fact / derived fact / inference / unknown / conflict
- `src/widgetware_sdr/skills.py` — loads a Skill's `skill.md` into a string
- `agents/qualification_agent.py` updated: `build_agent_instruction()` now calls `load_skill("icp_qualification")` instead of embedding the procedure as a string constant — the agent file itself now contains no qualification logic
- `tests/unit/` — updated to confirm the Skill is actually loaded (a specific phrase from `skill.md` appears in the instruction) rather than reimplemented inline

## Repository structure

```text
widgetware-sdr/
├── README.md / SPEC.md / pyproject.toml / .env.example
├── docs/
├── config/
├── data/sample_accounts/
├── skills/
│   ├── icp_qualification/
│   │   ├── skill.md
│   │   ├── examples/
│   │   └── tests/cases.yaml
│   └── evidence_classification/
│       └── skill.md
├── src/widgetware_sdr/
│   ├── skills.py
│   ├── app.py
│   └── agents/qualification_agent.py
├── tests/
│   ├── unit/
│   ├── integration/     # requires live credentials; skips otherwise
│   ├── contracts/        # populated starting Class 5
│   ├── scenarios/
│   └── fixtures/
└── scripts/check.sh
```

## Running the agent for real

Requires `GOOGLE_API_KEY` (or a configured Vertex AI project) in your environment:

```python
from widgetware_sdr.app import run_qualification_sync
import yaml

with open("data/sample_accounts/acme-001.yaml") as f:
    account = yaml.safe_load(f)

events = run_qualification_sync(account)
for event in events:
    print(event)
```

## Known failure cases

See [`KNOWN_FAILURE_CASES.md`](KNOWN_FAILURE_CASES.md) — in particular #1: a clean test run in this environment proves construction, not reasoning quality.

## Completion checklist

Before treating this checkpoint as done:

- [ ] `qualification_agent.py` contains no qualification procedure of its own — grep it for ICP-comparison logic; there should be none.
- [ ] `build_agent_instruction()` loads `skill.md` via `skills.py`, not a hardcoded string.
- [ ] The agent's static instruction still contains no specific account data anywhere.
- [ ] The agent still has no tools attached — confirmed by `test_agent_has_no_tools`.
- [ ] Both Skills have real, ordered procedures — not generic advice restating the goal.

## Starting Class 5

1. Start from this checkpoint. Class 5 does not touch `skills/`, `app.py`, or the agent's instruction assembly — it replaces the agent's *output* from free-form prose (`QUALIFY`/`DO_NOT_QUALIFY`/`NEEDS_RESEARCH` in a sentence) with a validated `QualificationResult` contract.
2. `skill.md`'s procedure still describes the reasoning; Class 5 only changes how the result is captured afterward.
3. See `../../class-05/` for what Class 5 adds.

## Status

- [x] Class 1 — Project charter, and the Antigravity workspace and repository harness
- [x] Class 2 — Gemini context and instruction architecture
- [x] Class 3 — First ADK agent (embedded procedure)
- [x] Class 4 — Skills and reusable agent capabilities
- [ ] Classes 5–10 — see `../../00_Course_Framework.md`
