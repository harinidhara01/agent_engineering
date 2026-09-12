import pytest
from pydantic import ValidationError

from widgetware_sdr.workflow.approval import (
    ApprovalDecision,
    ApprovalPackage,
    record_approval_decision,
)
from widgetware_sdr.workflow.state_machine import WorkflowState


def test_approve_produces_approved_state() -> None:
    assert record_approval_decision(ApprovalDecision.APPROVE) is WorkflowState.APPROVED


def test_reject_produces_rejected_state() -> None:
    assert record_approval_decision(ApprovalDecision.REJECT) is WorkflowState.REJECTED


def test_revise_returns_to_draft_ready() -> None:
    assert record_approval_decision(ApprovalDecision.REVISE) is WorkflowState.DRAFT_READY


def test_approval_package_contains_the_required_fields() -> None:
    package = ApprovalPackage(
        account_id="acme-001",
        qualification_summary="Matches ICP; strong pain signal.",
        supporting_evidence=["acme-001-ev-001"],
        proposed_outreach="Hi — following up on your recent digital-transformation initiative...",
        uncertainty_and_risk_flags=["employee count conflict between two sources"],
    )
    assert package.requested_action == "send_outreach"


def test_approval_package_rejects_unknown_fields() -> None:
    with pytest.raises(ValidationError):
        ApprovalPackage(
            account_id="acme-001",
            qualification_summary="Fits.",
            proposed_outreach="Draft text.",
            already_sent=True,  # not a real field — must not be silently accepted
        )
