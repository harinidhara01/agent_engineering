"""The batch loop, end to end — Book 1 §11's Hands-on Lab: a fresh
account gets selected and a settled one doesn't; a recoverable failure
retries up to the configured limit and no further; the loop stops at
both the account limit and a budget limit; every run's report names a
stop reason.

As in Class 7, `qualify`/`review`/`draft` are stub functions, not live
agents — see KNOWN_FAILURE_CASES.md. This suite's `review` stub is
written to be realistic about one thing specifically: it only approves
drafting for a QUALIFIED result, which is what actually stops a
disqualified account (brightleaf-002) from reaching AWAITING_APPROVAL
in these tests — the coordinator itself does not hard-code that rule;
the review stage does, exactly as Book 1 intends.
"""

from pathlib import Path

from widgetware_sdr.contracts.evidence_review import EvidenceReview
from widgetware_sdr.contracts.outreach_draft import OutreachDraft
from widgetware_sdr.contracts.qualification import QualificationResult, QualificationStatus
from widgetware_sdr.loop.account_queue import AccountQueue, QueuedAccount
from widgetware_sdr.loop.batch_runner import run_batch
from widgetware_sdr.loop.budget import Budget
from widgetware_sdr.workflow.state_machine import WorkflowState


def _stub_qualify(brief):
    if not brief.evidence_items:
        raise ValueError("no evidence to qualify from")
    # A tiny, honest stand-in for real qualification logic: look at the
    # account_id prefix, since our mock accounts are what they are.
    if brief.account_id == "brightleaf-002":
        return QualificationResult(
            account_id=brief.account_id,
            status=QualificationStatus.NOT_QUALIFIED,
            rationale="Excluded industry.",
            exclusion_reasons=["industry: financial_services is excluded"],
        )
    return QualificationResult(
        account_id=brief.account_id,
        status=QualificationStatus.QUALIFIED,
        rationale="Fits ICP.",
        evidence_refs=[brief.evidence_items[0].evidence_id],
    )


def _stub_review(brief, qualification):
    approved = qualification.status is QualificationStatus.QUALIFIED
    return EvidenceReview(
        account_id=brief.account_id,
        approved_claims=[c.text for c in brief.claims] if approved else [],
        rejected_claims=[] if approved else [c.text for c in brief.claims],
        sources_current=True,
        approved_for_drafting=approved and bool(brief.claims),
    )


def _stub_draft(review):
    return OutreachDraft(
        account_id=review.account_id, message="Draft.", used_claims=review.approved_claims
    )


def _seed_queue() -> AccountQueue:
    return AccountQueue(
        accounts=[
            QueuedAccount("acme-001"),
            QueuedAccount("brightleaf-002"),  # outside the ICP, deliberately
            QueuedAccount("meridian-003"),
            QueuedAccount("no-such-account"),
        ]
    )


def _generous_budget() -> Budget:
    return Budget(
        max_accounts_per_run=10,
        max_attempts_per_account=2,
        max_wall_clock_seconds=30.0,
        max_tool_calls=1000,
        max_consecutive_failures=10,
    )


def test_qualifying_account_reaches_awaiting_approval() -> None:
    queue = _seed_queue()
    run_batch(
        queue,
        qualify=_stub_qualify,
        review=_stub_review,
        draft=_stub_draft,
        budget=_generous_budget(),
    )
    acme = next(a for a in queue.accounts if a.account_id == "acme-001")
    assert acme.state is WorkflowState.AWAITING_APPROVAL


def test_disqualified_account_never_reaches_drafting() -> None:
    queue = _seed_queue()
    run_batch(
        queue,
        qualify=_stub_qualify,
        review=_stub_review,
        draft=_stub_draft,
        budget=_generous_budget(),
    )
    brightleaf = next(a for a in queue.accounts if a.account_id == "brightleaf-002")
    assert brightleaf.state is not WorkflowState.AWAITING_APPROVAL


def test_a_settled_account_is_not_reprocessed() -> None:
    queue = _seed_queue()
    run_batch(
        queue,
        qualify=_stub_qualify,
        review=_stub_review,
        draft=_stub_draft,
        budget=_generous_budget(),
    )
    acme = next(a for a in queue.accounts if a.account_id == "acme-001")
    attempts_after_first_run = acme.attempts

    # Run again with the same queue object — a settled account must not
    # be selected a second time.
    run_batch(
        queue,
        qualify=_stub_qualify,
        review=_stub_review,
        draft=_stub_draft,
        budget=_generous_budget(),
    )
    assert acme.attempts == attempts_after_first_run


def test_no_evidence_account_escalates_after_exhausting_retries() -> None:
    budget = Budget(
        max_accounts_per_run=20,
        max_attempts_per_account=2,
        max_wall_clock_seconds=30.0,
        max_tool_calls=1000,
        max_consecutive_failures=20,
    )
    queue = AccountQueue(accounts=[QueuedAccount("no-such-account")])
    report = run_batch(
        queue, qualify=_stub_qualify, review=_stub_review, draft=_stub_draft, budget=budget
    )

    account = queue.accounts[0]
    assert account.state is WorkflowState.NEEDS_HUMAN_REVIEW
    assert account.attempts == 2  # exactly the configured max, no more
    assert report.stop_reason == "no eligible accounts remain"


def test_stops_at_the_account_limit() -> None:
    budget = Budget(
        max_accounts_per_run=2,
        max_attempts_per_account=2,
        max_wall_clock_seconds=30.0,
        max_tool_calls=1000,
        max_consecutive_failures=10,
    )
    queue = _seed_queue()
    report = run_batch(
        queue, qualify=_stub_qualify, review=_stub_review, draft=_stub_draft, budget=budget
    )
    assert "max_accounts_per_run" in report.stop_reason


def test_stops_at_a_tool_call_budget() -> None:
    budget = Budget(
        max_accounts_per_run=100,
        max_attempts_per_account=2,
        max_wall_clock_seconds=30.0,
        max_tool_calls=1,
        max_consecutive_failures=10,
    )
    queue = _seed_queue()
    report = run_batch(
        queue, qualify=_stub_qualify, review=_stub_review, draft=_stub_draft, budget=budget
    )
    assert "max_tool_calls" in report.stop_reason


def test_every_run_names_a_stop_reason() -> None:
    queue = _seed_queue()
    report = run_batch(
        queue,
        qualify=_stub_qualify,
        review=_stub_review,
        draft=_stub_draft,
        budget=_generous_budget(),
    )
    assert report.stop_reason
    assert report.accounts_processed > 0


def test_checkpoints_are_written_per_account(tmp_path: Path) -> None:
    queue = _seed_queue()
    run_batch(
        queue,
        qualify=_stub_qualify,
        review=_stub_review,
        draft=_stub_draft,
        budget=_generous_budget(),
        checkpoint_dir=tmp_path,
    )
    assert (tmp_path / "acme-001.json").exists()
    assert (tmp_path / "brightleaf-002.json").exists()
