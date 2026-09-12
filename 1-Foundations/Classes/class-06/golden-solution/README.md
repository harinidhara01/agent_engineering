# WidgetWare SDR Lab

A bounded agent system that researches, qualifies, and drafts outreach to prospective manufacturing and industrial-automation accounts on WidgetWare's behalf — and stops for human approval before anything leaves the building.

This checkpoint (Class 6 / `golden-solutions/class-06/`) gives the agent its first real tools: three narrow, read-only functions for account, product, and ICP data, plus a deterministic fit-score helper kept outside model reasoning.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env  # fill in GOOGLE_API_KEY (or GOOGLE_CLOUD_PROJECT) to run the agent for real
./scripts/check.sh    # runs format check, lint, and tests — live-model tests skip automatically without credentials
```

## What's new this class

- `src/widgetware_sdr/tools/account_data.py` — `get_account_profile`, `get_widgetware_product`, `get_icp_policy`: three narrow, typed, read-only tools
- `src/widgetware_sdr/tools/fit_score.py` — `calculate_fit_score()`, a deterministic helper deliberately kept outside model reasoning
- `qualification_agent.py` updated: the three tools are attached, and the instruction now tells the model to use them instead of assuming facts, plus an explicit output-format instruction
- `tests/tools/` — 14 tool tests covering valid input, invalid input, missing record, and deterministic output shape

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
│   ├── tools/
│   │   ├── account_data.py
│   │   └── fit_score.py
│   └── agents/qualification_agent.py
├── tests/
│   ├── unit/
│   ├── contracts/
│   ├── tools/
│   ├── integration/       # requires live credentials; skips otherwise
│   ├── scenarios/
│   └── fixtures/
└── scripts/check.sh
```

## Known failure cases

See [`KNOWN_FAILURE_CASES.md`](KNOWN_FAILURE_CASES.md) — in particular #3: attaching tools doesn't prove the model actually uses them instead of its own assumptions; that requires a live run.

## Completion checklist

Before treating this checkpoint as done:

- [ ] All three tools return an `error_category`, not a raw exception, on invalid input or a missing record.
- [ ] `calculate_fit_score` is called nowhere the model could instead be asked to compute it — the arithmetic is application code, not a prompt.
- [ ] The agent's instruction explicitly tells the model to use the tools rather than assume account, product, or ICP facts (`test_instruction_tells_the_model_to_use_tools_not_assume_facts`).
- [ ] `QualificationResult`'s four business invariants (inherited from Class 5) still each have their own failing-case test.

## Starting Class 7

1. Start from this checkpoint. Class 7 adds the agent's first capability to look *outside* WidgetWare's own data — external research through a function tool — and the discipline to treat everything that comes back as untrusted until validated, the same isolation discipline Class 2 established for account notes.
2. The `QualificationResult` contract doesn't change structurally in Class 7, but the `EvidenceItem` contract gets real exercise: Class 7's research pipeline produces the first evidence items that didn't originate from a locally-supplied account note.
3. See `../../class-07/` for what Class 7 adds.

## Status

- [x] Class 1 — Project charter, and the Antigravity workspace and repository harness
- [x] Class 2 — Gemini context and instruction architecture
- [x] Class 3 — First ADK agent (embedded procedure)
- [x] Class 4 — Skills and reusable agent capabilities
- [x] Class 5 — Structured outputs and agent contracts
- [x] Class 6 — Tool engineering
- [ ] Classes 7–10 — see `../../00_Course_Framework.md`
