from widgetware_sdr.loop.run_report import RunReport
from widgetware_sdr.workflow.state_machine import WorkflowState


def test_run_report_always_names_a_stop_reason() -> None:
    report = RunReport.build(
        "run-1", "no eligible accounts remain", [WorkflowState.AWAITING_APPROVAL]
    )
    assert report.stop_reason == "no eligible accounts remain"


def test_run_report_counts_per_status_totals() -> None:
    report = RunReport.build(
        "run-1",
        "reached max_accounts_per_run (3)",
        [WorkflowState.AWAITING_APPROVAL, WorkflowState.AWAITING_APPROVAL, WorkflowState.BLOCKED],
    )
    assert report.status_totals["AWAITING_APPROVAL"] == 2
    assert report.status_totals["BLOCKED"] == 1
    assert report.accounts_processed == 3
