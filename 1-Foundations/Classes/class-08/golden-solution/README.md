# WidgetWare SDR Lab

A bounded agent system that researches, qualifies, and drafts outreach to prospective manufacturing and industrial-automation accounts on WidgetWare's behalf — and stops for human approval before anything leaves the building.

This checkpoint (Class 8 / `golden-solutions/class-08/`) composes everything built so far into a real multi-agent workflow — Research → Qualify → Review → Draft → Approve — with an explicit, validated state machine and a human approval gate no code path can bypass.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
./scripts/check.sh
```

## What's new this class

- `src/widgetware_sdr/workflow/state_machine.py` — the ten-state workflow, with an explicit allowed-transitions table; `SENT` does not exist as a state anywhere in this codebase
- `src/widgetware_sdr/workflow/approval.py` — `ApprovalPackage` and `record_approval_decision()`: approval produces a state change, never a side effect
- `src/widgetware_sdr/workflow/coordinator.py` — `run_workflow()`: sequences all five stages, checkpointing after each, never losing prior work on a failure
- `src/widgetware_sdr/contracts/evidence_review.py`, `contracts/outreach_draft.py` — the two new typed handoffs
- `src/widgetware_sdr/agents/evidence_reviewer.py`, `agents/drafting_agent.py` — two new ADK agents; the drafting agent structurally receives only approved claims, never the raw research
- `tests/workflow/` — 30 tests: state-machine transitions, approval, all five required scenarios, and checkpoint read/write

## Repository structure

```text
widgetware-sdr/
├── src/widgetware_sdr/
│   ├── contracts/
│   │   ├── evidence.py / qualification.py / research_brief.py
│   │   ├── evidence_review.py
│   │   └── outreach_draft.py
│   ├── workflow/
│   │   ├── state_machine.py
│   │   ├── approval.py
│   │   └── coordinator.py
│   └── agents/
│       ├── qualification_agent.py / research_agent.py
│       ├── evidence_reviewer.py
│       └── drafting_agent.py
├── tests/
│   ├── unit/ / contracts/ / tools/ / research/ / workflow/
│   └── integration/       # requires live credentials; skips otherwise
└── scripts/check.sh
```

## Trying the workflow

```python
from widgetware_sdr.workflow.coordinator import run_workflow
from widgetware_sdr.contracts.qualification import QualificationResult, QualificationStatus
from widgetware_sdr.contracts.evidence_review import EvidenceReview
from widgetware_sdr.contracts.outreach_draft import OutreachDraft


def qualify(brief):
    return QualificationResult(
        account_id=brief.account_id,
        status=QualificationStatus.QUALIFIED,
        rationale="Fits.",
        evidence_refs=[brief.evidence_items[0].evidence_id],
    )


def review(brief, qualification):
    return EvidenceReview(
        account_id=brief.account_id,
        approved_claims=[c.text for c in brief.claims],
        sources_current=True,
        approved_for_drafting=bool(brief.claims),
    )


def draft(evidence_review):
    return OutreachDraft(
        account_id=evidence_review.account_id,
        message="Draft.",
        used_claims=evidence_review.approved_claims,
    )


run = run_workflow({"account_id": "acme-001"}, qualify=qualify, review=review, draft=draft)
print(run.state)  # AWAITING_APPROVAL
```

The three functions above are stubs — in a live deployment they'd wrap the real `qualification_agent`, `evidence_reviewer`, and `drafting_agent`. See `KNOWN_FAILURE_CASES.md` #1 for exactly what that distinction does and doesn't prove at this checkpoint.

## Known failure cases

See [`KNOWN_FAILURE_CASES.md`](KNOWN_FAILURE_CASES.md) — in particular #5: nothing here actually tests resuming a workflow after a real process restart. That capability arrives in Class 10.

## Completion checklist

Before treating this checkpoint as done:

- [ ] `WorkflowState` has no state that could mean "sent" — verified by `test_sent_is_not_a_state_that_exists`.
- [ ] Every terminal state (`APPROVED`, `REJECTED`, `BLOCKED`) genuinely has zero outgoing transitions.
- [ ] All five required scenario tests pass: success, insufficient evidence, source conflict, malformed output, rejected approval.
- [ ] A `BLOCKED` run from a mid-workflow failure still has its `research_brief` populated — no partial work is lost.
- [ ] The Drafting Agent's instruction explicitly restricts it to approved claims only, and its description states it never sends anything.

## Starting Class 9

1. Start from this checkpoint. Class 9 asks whether this workflow is actually good enough to ship — a golden dataset, evaluation layers, release gates. The loop that processes a queue of accounts unattended comes one class later, in Class 10, only after this evaluation is in place.
2. `run_workflow()`'s single-account signature doesn't change in Class 9 or Class 10.
3. See `../../class-09/` for what Class 9 adds.

## Status

- [x] Class 1 — Project charter, and the Antigravity workspace and repository harness
- [x] Class 2 — Gemini context and instruction architecture
- [x] Class 3 — First ADK agent (embedded procedure)
- [x] Class 4 — Skills and reusable agent capabilities
- [x] Class 5 — Structured outputs and agent contracts
- [x] Class 6 — Tool engineering
- [x] Class 7 — MCP and evidence-backed research
- [x] Class 8 — Multi-agent workflow and human approval
- [ ] Classes 9–10 — see `../../00_Course_Framework.md`
