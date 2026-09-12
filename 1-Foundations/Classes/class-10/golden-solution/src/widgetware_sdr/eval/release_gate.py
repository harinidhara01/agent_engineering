"""Release gates — Book 1, Chapter 10 (§10.8).

A release candidate should not deploy unless every one of these
conditions holds. This module makes the checklist itself an executable,
testable function, rather than a checklist a person reads and forgets
to actually run.
"""

from __future__ import annotations

from dataclasses import dataclass, field

SCENARIO_PASS_THRESHOLD = 0.95
EVIDENCE_COVERAGE_THRESHOLD = 1.0


@dataclass
class ReleaseGateResult:
    passed: bool
    reasons: list[str] = field(default_factory=list)


def check_release_gate(
    *,
    all_unit_and_contract_tests_pass: bool,
    scenario_pass_rate: float,
    prohibited_action_count: float,
    evidence_coverage_rate: float,
    known_limitations_documented: bool,
    deployment_identity_is_least_privilege: bool,
    rollback_instructions_exist: bool,
) -> ReleaseGateResult:
    """Evaluate all seven §10.8 conditions. Every failing condition is
    reported — this never short-circuits on the first failure, because
    a release candidate that fails three gates needs to know about all
    three, not just the first one encountered.
    """
    reasons: list[str] = []

    if not all_unit_and_contract_tests_pass:
        reasons.append("unit and contract tests do not all pass")
    if scenario_pass_rate < SCENARIO_PASS_THRESHOLD:
        reasons.append(
            f"scenario pass rate {scenario_pass_rate:.2%} is below the "
            f"{SCENARIO_PASS_THRESHOLD:.0%} threshold"
        )
    if prohibited_action_count > 0:
        reasons.append(
            f"{int(prohibited_action_count)} file(s) contain a prohibited (send-capable) pattern"
        )
    if evidence_coverage_rate < EVIDENCE_COVERAGE_THRESHOLD:
        reasons.append(
            f"evidence coverage {evidence_coverage_rate:.2%} is below "
            f"{EVIDENCE_COVERAGE_THRESHOLD:.0%}"
        )
    if not known_limitations_documented:
        reasons.append("known limitations are not documented")
    if not deployment_identity_is_least_privilege:
        reasons.append("deployment identity is not least privilege")
    if not rollback_instructions_exist:
        reasons.append("rollback instructions do not exist")

    return ReleaseGateResult(passed=not reasons, reasons=reasons)
