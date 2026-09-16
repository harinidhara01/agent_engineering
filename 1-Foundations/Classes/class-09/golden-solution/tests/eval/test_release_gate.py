from widgetware_sdr.eval.release_gate import check_release_gate

GOOD_ARGS = dict(
    all_unit_and_contract_tests_pass=True,
    scenario_pass_rate=0.98,
    prohibited_action_count=0.0,
    evidence_coverage_rate=1.0,
    known_limitations_documented=True,
    deployment_identity_is_least_privilege=True,
    rollback_instructions_exist=True,
)


def test_all_conditions_met_passes() -> None:
    result = check_release_gate(**GOOD_ARGS)
    assert result.passed is True
    assert result.reasons == []


def test_failing_tests_fails_the_gate() -> None:
    args = dict(GOOD_ARGS, all_unit_and_contract_tests_pass=False)
    result = check_release_gate(**args)
    assert result.passed is False
    assert any("tests" in r for r in result.reasons)


def test_low_scenario_pass_rate_fails_the_gate() -> None:
    args = dict(GOOD_ARGS, scenario_pass_rate=0.80)
    result = check_release_gate(**args)
    assert result.passed is False


def test_a_prohibited_action_pattern_fails_the_gate() -> None:
    args = dict(GOOD_ARGS, prohibited_action_count=1.0)
    result = check_release_gate(**args)
    assert result.passed is False
    assert any("prohibited" in r for r in result.reasons)


def test_multiple_failures_are_all_reported_not_just_the_first() -> None:
    args = dict(
        GOOD_ARGS, all_unit_and_contract_tests_pass=False, rollback_instructions_exist=False
    )
    result = check_release_gate(**args)
    assert len(result.reasons) == 2
