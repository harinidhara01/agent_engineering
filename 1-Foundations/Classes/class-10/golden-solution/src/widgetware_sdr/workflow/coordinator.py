"""Workflow orchestration — Book 1, Chapter 9.

Composes Research → Qualify → Review → Draft → Approve into one
sequenced run, always through `state_machine.transition()`, always
checkpointing after each stage. The final state is `AWAITING_APPROVAL`
or a named failure state — never anything resembling "sent."

The qualify, review, and draft stages are model-backed in a live
deployment, but this coordinator takes them as injected callables
rather than calling a specific agent directly. That is not a shortcut —
it is what makes the state machine, checkpointing, and partial-failure
handling in this module fully testable without a live model call,
while still being exactly what a live wiring (agents/*.py plus a real
Gemini call) would plug into unchanged.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Callable

from widgetware_sdr.contracts.evidence_review import EvidenceReview
from widgetware_sdr.contracts.outreach_draft import OutreachDraft
from widgetware_sdr.contracts.qualification import QualificationResult
from widgetware_sdr.contracts.research_brief import ResearchBrief
from widgetware_sdr.research import build_research_brief
from widgetware_sdr.workflow.state_machine import IllegalTransitionError, WorkflowState, transition

QualifyFn = Callable[[ResearchBrief], QualificationResult]
ReviewFn = Callable[[ResearchBrief, QualificationResult], EvidenceReview]
DraftFn = Callable[[EvidenceReview], OutreachDraft]


@dataclass
class WorkflowRun:
    account_id: str
    state: WorkflowState = WorkflowState.RECEIVED
    research_brief: ResearchBrief | None = None
    qualification_result: QualificationResult | None = None
    evidence_review: EvidenceReview | None = None
    outreach_draft: OutreachDraft | None = None
    stop_reason: str | None = None
    history: list[str] = field(default_factory=list)

    def advance(self, next_state: WorkflowState) -> None:
        self.state = transition(self.state, next_state)
        self.history.append(self.state.value)


def run_workflow(
    account: dict,
    qualify: QualifyFn,
    review: ReviewFn,
    draft: DraftFn,
    checkpoint_dir: Path | None = None,
) -> WorkflowRun:
    """Run the full workflow for one account, checkpointing after each
    stage. Never raises on an expected business failure (insufficient
    evidence, malformed output) — those produce a `BLOCKED` run with a
    `stop_reason`, per Book 1 §9.7: each failure should produce a
    visible state and next action, not an exception that loses prior
    successful work.
    """
    run = WorkflowRun(account_id=account["account_id"])
    _checkpoint(run, checkpoint_dir)

    run.advance(WorkflowState.RESEARCHING)
    run.research_brief = build_research_brief(account)
    if not run.research_brief.evidence_items:
        run.stop_reason = "insufficient evidence: no research results"
        run.advance(WorkflowState.BLOCKED)
        _checkpoint(run, checkpoint_dir)
        return run
    run.advance(WorkflowState.RESEARCH_COMPLETE)
    _checkpoint(run, checkpoint_dir)

    run.advance(WorkflowState.QUALIFYING)
    try:
        run.qualification_result = qualify(run.research_brief)
    except Exception as exc:  # noqa: BLE001 — deliberately broad: any qualify() failure is a workflow-level BLOCKED, not a crash
        run.stop_reason = f"qualification failed: {exc}"
        run.advance(WorkflowState.BLOCKED)
        _checkpoint(run, checkpoint_dir)
        return run
    run.advance(WorkflowState.REVIEW_REQUIRED)
    _checkpoint(run, checkpoint_dir)

    run.evidence_review = review(run.research_brief, run.qualification_result)
    if not run.evidence_review.approved_for_drafting:
        run.stop_reason = "evidence review did not approve drafting"
        run.advance(WorkflowState.BLOCKED)
        _checkpoint(run, checkpoint_dir)
        return run
    run.advance(WorkflowState.DRAFT_READY)
    _checkpoint(run, checkpoint_dir)

    run.outreach_draft = draft(run.evidence_review)
    run.advance(WorkflowState.AWAITING_APPROVAL)
    _checkpoint(run, checkpoint_dir)

    return run


def _checkpoint(run: WorkflowRun, checkpoint_dir: Path | None) -> None:
    if checkpoint_dir is None:
        return
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    path = checkpoint_dir / f"{run.account_id}.json"
    payload = {
        "account_id": run.account_id,
        "state": run.state.value,
        "stop_reason": run.stop_reason,
        "history": run.history,
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def load_checkpoint(checkpoint_dir: Path, account_id: str) -> dict:
    path = checkpoint_dir / f"{account_id}.json"
    return json.loads(path.read_text(encoding="utf-8"))


__all__ = [
    "WorkflowRun",
    "run_workflow",
    "load_checkpoint",
    "IllegalTransitionError",
    "asdict",
]
