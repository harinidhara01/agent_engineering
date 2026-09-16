from widgetware_sdr.contracts.qualification import QualificationResult, QualificationStatus
from widgetware_sdr.eval.metrics import (
    approval_compliance_rate,
    contract_validity_rate,
    evidence_coverage_rate,
    prohibited_action_rate,
)
from widgetware_sdr.workflow.coordinator import WorkflowRun
from widgetware_sdr.workflow.state_machine import WorkflowState


def test_prohibited_action_rate_is_zero_across_the_real_codebase() -> None:
    """The actual, meaningful assertion: scanning this checkpoint's own
    source finds no send-capable code anywhere.
    """
    assert prohibited_action_rate() == 0.0


def test_contract_validity_rate_for_all_successful_runs() -> None:
    runs = [WorkflowRun(account_id="a", state=WorkflowState.AWAITING_APPROVAL) for _ in range(3)]
    assert contract_validity_rate(runs) == 1.0


def test_contract_validity_rate_counts_blocked_runs_as_invalid() -> None:
    runs = [
        WorkflowRun(account_id="a", state=WorkflowState.AWAITING_APPROVAL),
        WorkflowRun(account_id="b", state=WorkflowState.BLOCKED),
    ]
    assert contract_validity_rate(runs) == 0.5


def test_contract_validity_rate_with_no_runs_defaults_to_perfect() -> None:
    assert contract_validity_rate([]) == 1.0


def test_evidence_coverage_rate_for_qualified_results() -> None:
    qualified_with_evidence = QualificationResult(
        account_id="a",
        status=QualificationStatus.QUALIFIED,
        rationale="Fits.",
        evidence_refs=["ev-1"],
    )
    run = WorkflowRun(account_id="a", qualification_result=qualified_with_evidence)
    assert evidence_coverage_rate([run]) == 1.0


def test_evidence_coverage_rate_ignores_non_qualified_results() -> None:
    not_qualified = QualificationResult(
        account_id="b",
        status=QualificationStatus.NOT_QUALIFIED,
        rationale="Excluded.",
        exclusion_reasons=["industry"],
    )
    run = WorkflowRun(account_id="b", qualification_result=not_qualified)
    assert (
        evidence_coverage_rate([run]) == 1.0
    )  # no qualified results to check, defaults to perfect


def test_approval_compliance_rate_counts_named_terminal_or_awaiting_states() -> None:
    runs = [
        WorkflowRun(account_id="a", state=WorkflowState.AWAITING_APPROVAL),
        WorkflowRun(account_id="b", state=WorkflowState.REJECTED),
    ]
    assert approval_compliance_rate(runs) == 1.0
