"""Coordinator scenario tests — Book 1 §9's Hands-on Lab: success,
insufficient evidence, source conflict, malformed output, and rejected
approval.

`qualify`, `review`, and `draft` are injected as plain stub functions
here — this is what makes the state machine, checkpointing, and
partial-failure handling in coordinator.py fully testable without a
live model call. See KNOWN_FAILURE_CASES.md for what this does and
does not prove about the real agents.
"""

from widgetware_sdr.contracts.evidence_review import EvidenceReview
from widgetware_sdr.contracts.outreach_draft import OutreachDraft
from widgetware_sdr.contracts.qualification import QualificationResult, QualificationStatus
from widgetware_sdr.workflow.approval import ApprovalDecision, record_approval_decision
from widgetware_sdr.workflow.coordinator import run_workflow
from widgetware_sdr.workflow.state_machine import WorkflowState

ACME = {"account_id": "acme-001", "company_name": "Acme Manufacturing"}
NO_EVIDENCE_ACCOUNT = {"account_id": "no-such-account", "company_name": "Nobody Corp"}


def _stub_qualify_success(brief):
    return QualificationResult(
        account_id=brief.account_id,
        status=QualificationStatus.QUALIFIED,
        rationale="Matches ICP.",
        evidence_refs=[brief.evidence_items[0].evidence_id],
    )


def _stub_review_approves(brief, qualification):
    return EvidenceReview(
        account_id=brief.account_id,
        approved_claims=[c.text for c in brief.claims],
        sources_current=True,
        approved_for_drafting=bool(brief.claims),
    )


def _stub_draft(review):
    return OutreachDraft(
        account_id=review.account_id,
        message="Hi — following up given: " + "; ".join(review.approved_claims[:1]),
        used_claims=review.approved_claims,
    )


def test_success_scenario_reaches_awaiting_approval() -> None:
    run = run_workflow(
        ACME, qualify=_stub_qualify_success, review=_stub_review_approves, draft=_stub_draft
    )
    assert run.state is WorkflowState.AWAITING_APPROVAL
    assert run.outreach_draft is not None
    assert run.stop_reason is None


def test_insufficient_evidence_scenario_blocks_before_qualification() -> None:
    run = run_workflow(
        NO_EVIDENCE_ACCOUNT,
        qualify=_stub_qualify_success,
        review=_stub_review_approves,
        draft=_stub_draft,
    )
    assert run.state is WorkflowState.BLOCKED
    assert "insufficient evidence" in run.stop_reason
    assert run.qualification_result is None  # never reached that stage


def test_source_conflict_scenario_preserves_the_conflict_through_the_run() -> None:
    """Book 1 §8.4's conflict, still visible after Chapter 9 composes
    the stages — never silently dropped on the way to qualification.
    """
    run = run_workflow(
        ACME, qualify=_stub_qualify_success, review=_stub_review_approves, draft=_stub_draft
    )
    assert len(run.research_brief.conflicts) == 1
    assert run.state is WorkflowState.AWAITING_APPROVAL  # a conflict doesn't halt the run by itself


def test_malformed_output_scenario_blocks_without_losing_research() -> None:
    def _stub_qualify_raises(brief):
        raise ValueError("malformed qualification output")

    run = run_workflow(
        ACME, qualify=_stub_qualify_raises, review=_stub_review_approves, draft=_stub_draft
    )
    assert run.state is WorkflowState.BLOCKED
    assert "qualification failed" in run.stop_reason
    # Book 1 §9.7: a failure should not lose prior successful work.
    assert run.research_brief is not None
    assert len(run.research_brief.evidence_items) > 0


def test_rejected_approval_scenario_does_not_proceed() -> None:
    run = run_workflow(
        ACME, qualify=_stub_qualify_success, review=_stub_review_approves, draft=_stub_draft
    )
    assert run.state is WorkflowState.AWAITING_APPROVAL

    final_state = record_approval_decision(ApprovalDecision.REJECT)
    assert final_state is WorkflowState.REJECTED
    # Confirming this is a legal transition from where the run actually is.
    from widgetware_sdr.workflow.state_machine import validate_transition

    assert validate_transition(run.state, final_state)


def test_evidence_review_rejecting_everything_blocks_before_drafting() -> None:
    def _stub_review_rejects_all(brief, qualification):
        return EvidenceReview(
            account_id=brief.account_id,
            approved_claims=[],
            rejected_claims=[c.text for c in brief.claims],
            sources_current=True,
            approved_for_drafting=False,
        )

    run = run_workflow(
        ACME, qualify=_stub_qualify_success, review=_stub_review_rejects_all, draft=_stub_draft
    )
    assert run.state is WorkflowState.BLOCKED
    assert run.outreach_draft is None
