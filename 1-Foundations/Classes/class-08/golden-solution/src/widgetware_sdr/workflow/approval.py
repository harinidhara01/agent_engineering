"""Human-in-the-loop approval — Book 1, Chapter 9 (§9.6).

Approval is a workflow state and policy decision, not an instruction
asking a model to "check with the user first." The system remains
structurally unable to execute the external action without an approved
state — because no code anywhere in this repository executes that
action even once approval is granted. Approval only ever produces a
state change, never a side effect.
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field

from widgetware_sdr.workflow.state_machine import WorkflowState


class ApprovalDecision(str, Enum):
    APPROVE = "APPROVE"
    REJECT = "REJECT"
    REVISE = "REVISE"


class ApprovalPackage(BaseModel):
    """Everything a human needs to decide, in one place — Book 1 §9.6's
    required contents, as a typed contract.
    """

    model_config = {"extra": "forbid"}

    account_id: str
    qualification_summary: str
    supporting_evidence: list[str] = Field(default_factory=list)
    proposed_outreach: str
    uncertainty_and_risk_flags: list[str] = Field(default_factory=list)
    requested_action: str = "send_outreach"


def record_approval_decision(decision: ApprovalDecision) -> WorkflowState:
    """Map a human's decision to the resulting workflow state.

    This function's return value is a *state*, never an action. Nothing
    downstream of this function sends anything — there is nothing
    downstream of this function at all, in this book.
    """
    if decision is ApprovalDecision.APPROVE:
        return WorkflowState.APPROVED
    if decision is ApprovalDecision.REJECT:
        return WorkflowState.REJECTED
    return WorkflowState.DRAFT_READY  # REVISE: back to drafting, not a dead end
