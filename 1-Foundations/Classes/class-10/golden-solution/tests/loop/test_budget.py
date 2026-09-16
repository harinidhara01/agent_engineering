from widgetware_sdr.loop.budget import Budget, BudgetUsage, budget_exceeded

BUDGET = Budget(
    max_accounts_per_run=3,
    max_attempts_per_account=2,
    max_wall_clock_seconds=60.0,
    max_tool_calls=100,
    max_consecutive_failures=2,
)


def test_within_budget_returns_none() -> None:
    usage = BudgetUsage(
        accounts_processed=1, tool_calls=5, consecutive_failures=0, elapsed_seconds=1.0
    )
    assert budget_exceeded(BUDGET, usage) is None


def test_max_accounts_reached() -> None:
    usage = BudgetUsage(accounts_processed=3)
    reason = budget_exceeded(BUDGET, usage)
    assert reason is not None
    assert "max_accounts_per_run" in reason


def test_max_consecutive_failures_reached() -> None:
    usage = BudgetUsage(consecutive_failures=2)
    reason = budget_exceeded(BUDGET, usage)
    assert "max_consecutive_failures" in reason


def test_max_wall_clock_reached() -> None:
    usage = BudgetUsage(elapsed_seconds=61.0)
    reason = budget_exceeded(BUDGET, usage)
    assert "max_wall_clock_seconds" in reason
