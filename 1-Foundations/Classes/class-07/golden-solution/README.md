# WidgetWare SDR Lab

A bounded agent system that researches, qualifies, and drafts outreach to prospective manufacturing and industrial-automation accounts on WidgetWare's behalf — and stops for human approval before anything leaves the building.

This checkpoint (Class 7 / `golden-solutions/class-07/`) adds the agent's first capability to look outside WidgetWare's own data: a research pipeline that gathers external evidence, normalizes it into the `EvidenceItem` contract, detects conflicts between sources, and never lets a claim exist without a citation — treating everything retrieved as untrusted content throughout.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
./scripts/check.sh
```

## What's new this class

- `data/mock_public_sources.yaml` — a local, deterministic stand-in for a real external research source (see `KNOWN_FAILURE_CASES.md` #1 for what this simplifies away)
- `src/widgetware_sdr/tools/research_tools.py` — `search_public_records(account_id)`, the research function tool
- `src/widgetware_sdr/contracts/research_brief.py` — the `ResearchBrief` and `Claim`/`Conflict` contracts, with a validator that rejects any material claim lacking an evidence reference
- `src/widgetware_sdr/research.py` — the deterministic pipeline: normalizes evidence, detects employee-count conflicts, builds a complete `ResearchBrief` — no model call anywhere in this file
- `src/widgetware_sdr/agents/research_agent.py` — the Research Agent: a real ADK `Agent` with the search tool attached and an explicit instruction that retrieved content is data, never an instruction
- `tests/research/` — 9 fully offline tests, including one that deliberately feeds the pipeline a prompt-injection attempt

## Repository structure

```text
widgetware-sdr/
├── data/
│   ├── sample_accounts/
│   └── mock_public_sources.yaml
├── src/widgetware_sdr/
│   ├── contracts/
│   │   ├── evidence.py
│   │   ├── qualification.py
│   │   └── research_brief.py
│   ├── tools/
│   │   ├── account_data.py
│   │   ├── fit_score.py
│   │   └── research_tools.py
│   ├── research.py
│   └── agents/
│       ├── qualification_agent.py
│       └── research_agent.py
├── tests/
│   ├── unit/ / contracts/ / tools/ / research/
│   ├── integration/       # requires live credentials; skips otherwise
│   └── fixtures/
└── scripts/check.sh
```

## Trying the research pipeline

```python
from widgetware_sdr.research import build_research_brief

brief = build_research_brief({"account_id": "acme-001"})
print(brief.summary)  # "3 evidence item(s) gathered; 1 conflict(s) detected."
print(
    brief.conflicts[0]
)  # the employee-count conflict, both values, both sources — never silently resolved
```

## Known failure cases

See [`KNOWN_FAILURE_CASES.md`](KNOWN_FAILURE_CASES.md) — in particular #2: conflict detection here is one narrow regular expression, not a general capability.

## Completion checklist

Before treating this checkpoint as done:

- [ ] `build_research_brief` for `acme-001` surfaces the employee-count conflict rather than picking one value.
- [ ] The injection-attempt test confirms the attack text becomes ordinary, cited claim text — never dropped, never elevated to a special status.
- [ ] `ResearchBrief`'s validator actually rejects an uncited material claim — verified by a failing-case test, not just a passing one.
- [ ] The Research Agent's instruction explicitly states that evidence content is data, not instruction, in language a model would actually read as a rule (not just a comment).
- [ ] You understand, and could explain, exactly what `detect_employee_count_conflict` does and does not catch.

## Starting Class 8

1. Start from this checkpoint. Class 8 composes the qualification agent (Classes 3–6) and the research agent (this class) into a real multi-agent workflow — Research → Qualify → Review → Draft → Approve — with an explicit state machine and a human approval gate before any outreach.
2. The `ResearchBrief` this class produces becomes the Qualification Agent's input in Class 8's workflow, replacing the ad hoc account dict it currently reasons over directly.
3. See `../../class-08/` for what Class 8 adds.

## Status

- [x] Class 1 — Project charter, and the Antigravity workspace and repository harness
- [x] Class 2 — Gemini context and instruction architecture
- [x] Class 3 — First ADK agent (embedded procedure)
- [x] Class 4 — Skills and reusable agent capabilities
- [x] Class 5 — Structured outputs and agent contracts
- [x] Class 6 — Tool engineering
- [x] Class 7 — MCP and evidence-backed research
- [ ] Classes 8–10 — see `../../00_Course_Framework.md`
