from widgetware_sdr.loop.account_queue import AccountQueue, QueuedAccount
from widgetware_sdr.workflow.state_machine import WorkflowState


def test_select_next_returns_a_fresh_account() -> None:
    queue = AccountQueue(accounts=[QueuedAccount("acme-001")])
    assert queue.select_next().account_id == "acme-001"


def test_select_next_skips_a_settled_account() -> None:
    queue = AccountQueue(
        accounts=[
            QueuedAccount("acme-001", state=WorkflowState.APPROVED),
            QueuedAccount("brightleaf-002", state=WorkflowState.RECEIVED),
        ]
    )
    assert queue.select_next().account_id == "brightleaf-002"


def test_select_next_returns_none_when_all_settled() -> None:
    queue = AccountQueue(accounts=[QueuedAccount("acme-001", state=WorkflowState.APPROVED)])
    assert queue.select_next() is None


def test_retry_pending_is_eligible_again() -> None:
    queue = AccountQueue(accounts=[QueuedAccount("acme-001", state=WorkflowState.RETRY_PENDING)])
    assert queue.select_next() is not None


def test_exclude_set_skips_deferred_accounts_without_changing_their_state() -> None:
    queue = AccountQueue(
        accounts=[
            QueuedAccount("acme-001", state=WorkflowState.RECEIVED),
            QueuedAccount("brightleaf-002", state=WorkflowState.RECEIVED),
        ]
    )
    selected = queue.select_next(exclude={"acme-001"})
    assert selected.account_id == "brightleaf-002"
    assert queue.accounts[0].state is WorkflowState.RECEIVED  # unchanged, still eligible next run


def test_is_settled_reflects_current_state() -> None:
    queue = AccountQueue(accounts=[QueuedAccount("acme-001", state=WorkflowState.REJECTED)])
    assert queue.is_settled("acme-001") is True
    assert queue.is_settled("unknown-account") is False


def test_remaining_eligible_count() -> None:
    queue = AccountQueue(
        accounts=[
            QueuedAccount("a", state=WorkflowState.RECEIVED),
            QueuedAccount("b", state=WorkflowState.APPROVED),
            QueuedAccount("c", state=WorkflowState.RETRY_PENDING),
        ]
    )
    assert queue.remaining_eligible_count() == 2
