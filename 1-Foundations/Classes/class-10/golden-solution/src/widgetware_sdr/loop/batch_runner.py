"""The engineered batch loop — Book 1, Chapter 11.

`run_batch` is the outer loop: select an account, run the Chapter 9
workflow for it, verify the outcome, decide what happens next, persist
state, repeat — until the budget or the queue runs out. It wraps
Chapter 9's `run_workflow` unchanged; nothing about the single-account
workflow is modified here.

`create_batch_loop_agent` wires the same workflow into ADK's own
`LoopAgent` primitive, for a real ADK-native deployment. See
KNOWN_FAILURE_CASES.md for the deprecation warning the installed ADK
version emits for `LoopAgent` — a live discrepancy between this
chapter's teaching and the SDK's current direction.
"""

from __future__ import annotations

import time
import uuid
from pathlib import Path

from google.adk.agents import Agent, LoopAgent

from widgetware_sdr.instructions import get_model_id
from widgetware_sdr.loop.account_queue import AccountQueue
from widgetware_sdr.loop.budget import Budget, BudgetUsage, budget_exceeded
from widgetware_sdr.loop.decision import LoopDecision, decide
from widgetware_sdr.loop.run_report import RunReport
from widgetware_sdr.workflow.coordinator import DraftFn, QualifyFn, ReviewFn, run_workflow
from widgetware_sdr.workflow.state_machine import WorkflowState, transition


def run_batch(
    queue: AccountQueue,
    qualify: QualifyFn,
    review: ReviewFn,
    draft: DraftFn,
    budget: Budget,
    checkpoint_dir: Path | None = None,
) -> RunReport:
    """Process the queue until the budget or eligible work runs out.
    Returns a report naming exactly one stop reason, always.
    """
    usage = BudgetUsage()
    final_states: list[WorkflowState] = []
    deferred_this_run: set[str] = set()
    run_id = uuid.uuid4().hex[:8]
    start = time.perf_counter()

    while True:
        usage.elapsed_seconds = time.perf_counter() - start
        reason = budget_exceeded(budget, usage)
        if reason:
            return RunReport.build(run_id, reason, final_states)

        account = queue.select_next(exclude=deferred_this_run)
        if account is None:
            stop_reason = (
                "no eligible accounts remain"
                if not deferred_this_run
                else "no eligible accounts remain (some deferred to next run)"
            )
            return RunReport.build(run_id, stop_reason, final_states)

        account.attempts += 1
        usage.accounts_processed += 1
        # A coarse stand-in for real per-call tracking: this checkpoint
        # doesn't inspect the live ADK event stream for actual tool_call
        # events (that requires a real model run — see Class 4's
        # app.py), so one workflow run is counted as one tool call here.
        # See KNOWN_FAILURE_CASES.md #1 for what this simplifies away.
        usage.tool_calls += 1

        run = run_workflow(
            {"account_id": account.account_id},
            qualify=qualify,
            review=review,
            draft=draft,
            checkpoint_dir=checkpoint_dir,
        )

        # Verification before advancing (§11.7): trust only the state
        # the Chapter 9 state machine actually reached, not an
        # assumption about what should have happened.
        account.state = run.state

        decision = decide(
            account_state=account.state,
            attempts=account.attempts,
            max_attempts_per_account=budget.max_attempts_per_account,
            budget_exceeded_reason=budget_exceeded(budget, usage),
        )

        if decision is LoopDecision.STOP:
            final_states.append(account.state)
            return RunReport.build(
                run_id, budget_exceeded(budget, usage) or "stopped", final_states
            )

        if decision is LoopDecision.RETRY:
            account.state = transition(account.state, WorkflowState.RETRY_PENDING)
            usage.consecutive_failures += 1
            continue

        if decision is LoopDecision.ESCALATE:
            if account.state is WorkflowState.BLOCKED:
                account.state = transition(account.state, WorkflowState.NEEDS_HUMAN_REVIEW)
            usage.consecutive_failures = 0
            final_states.append(account.state)
            continue

        if decision is LoopDecision.DEFER:
            deferred_this_run.add(account.account_id)
            continue

        # CONTINUE
        usage.consecutive_failures = 0
        final_states.append(account.state)


def create_batch_loop_agent(max_iterations: int) -> LoopAgent:
    """The ADK-native version of the same loop, for a real deployment.

    A `LoopAgent` executes its sub-agents repeatedly, passing the same
    `InvocationContext` through each iteration so state persists across
    iterations. It is deterministic in *how* it iterates, even though
    the sub-agent it wraps reasons with a model.
    """
    workflow_agent = Agent(
        name="widgetware_workflow",
        model=get_model_id(),
        instruction=(
            "Process one account through the WidgetWare workflow: research, "
            "qualify, review, draft, and stop at AWAITING_APPROVAL or a named "
            "failure state. Never attempt to send anything — no such capability exists."
        ),
    )
    return LoopAgent(
        name="widgetware_batch_loop",
        sub_agents=[workflow_agent],
        max_iterations=max_iterations,
    )
