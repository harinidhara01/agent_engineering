from widgetware_sdr.contracts.evidence_review import EvidenceReview
from widgetware_sdr.contracts.outreach_draft import OutreachDraft
from widgetware_sdr.contracts.qualification import QualificationResult, QualificationStatus
from widgetware_sdr.workflow.coordinator import load_checkpoint, run_workflow
from widgetware_sdr.workflow.state_machine import WorkflowState

ACME = {"account_id": "acme-001", "company_name": "Acme Manufacturing"}


def _stub_qualify(brief):
    return QualificationResult(
        account_id=brief.account_id,
        status=QualificationStatus.QUALIFIED,
        rationale="Fits.",
        evidence_refs=[brief.evidence_items[0].evidence_id],
    )


def _stub_review(brief, qualification):
    return EvidenceReview(
        account_id=brief.account_id,
        approved_claims=[c.text for c in brief.claims],
        sources_current=True,
        approved_for_drafting=bool(brief.claims),
    )


def _stub_draft(review):
    return OutreachDraft(
        account_id=review.account_id, message="Draft.", used_claims=review.approved_claims
    )


def test_checkpoint_is_written_after_each_stage(tmp_path) -> None:
    run_workflow(
        ACME, qualify=_stub_qualify, review=_stub_review, draft=_stub_draft, checkpoint_dir=tmp_path
    )

    checkpoint = load_checkpoint(tmp_path, "acme-001")
    assert checkpoint["state"] == WorkflowState.AWAITING_APPROVAL.value
    # Every intermediate state the run passed through is recorded, not
    # just the final one — this is what "resume" would read to decide
    # what already happened.
    assert WorkflowState.RESEARCH_COMPLETE.value in checkpoint["history"]
    assert WorkflowState.REVIEW_REQUIRED.value in checkpoint["history"]


def test_checkpoint_for_a_blocked_run_records_the_stop_reason(tmp_path) -> None:
    run_workflow(
        {"account_id": "no-such-account"},
        qualify=_stub_qualify,
        review=_stub_review,
        draft=_stub_draft,
        checkpoint_dir=tmp_path,
    )
    checkpoint = load_checkpoint(tmp_path, "no-such-account")
    assert checkpoint["state"] == WorkflowState.BLOCKED.value
    assert checkpoint["stop_reason"] is not None
