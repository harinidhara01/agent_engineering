from widgetware_sdr.context_builder import load_config
from widgetware_sdr.tools.fit_score import calculate_fit_score

ICP = load_config("icp.yaml")


def test_qualifying_account_scores_the_full_weight() -> None:
    account = {
        "industry": "manufacturing",
        "employee_count": 22000,
        "region": "united_states",
        "known_challenges": ["legacy plant-floor systems"],
    }
    assert calculate_fit_score(account, ICP) == 1.0


def test_excluded_industry_scores_zero_regardless_of_other_attributes() -> None:
    account = {
        "industry": "financial_services",
        "employee_count": 50000,
        "region": "united_states",
        "known_challenges": ["something"],
    }
    assert calculate_fit_score(account, ICP) == 0.0


def test_unknown_employee_count_contributes_neither_pass_nor_fail() -> None:
    with_known = calculate_fit_score(
        {"industry": "industrial_automation", "employee_count": 6000, "region": "europe"}, ICP
    )
    with_unknown = calculate_fit_score(
        {"industry": "industrial_automation", "employee_count": None, "region": "europe"}, ICP
    )
    # Unknown scores lower than a confirmed pass, but the function does
    # not raise, and does not treat None as a confirmed fail either —
    # it simply contributes 0 to that one component.
    assert with_unknown < with_known
    assert with_unknown >= 0.0


def test_exactly_at_the_minimum_employee_count_counts_as_meeting_it() -> None:
    account = {
        "industry": "manufacturing",
        "employee_count": ICP["minimum_employee_count"],
        "region": "india",
    }
    score_at_threshold = calculate_fit_score(account, ICP)

    just_below = dict(account, employee_count=ICP["minimum_employee_count"] - 1)
    score_below = calculate_fit_score(just_below, ICP)

    assert score_at_threshold > score_below


def test_score_is_deterministic() -> None:
    account = {"industry": "manufacturing", "employee_count": 10000, "region": "united_states"}
    assert calculate_fit_score(account, ICP) == calculate_fit_score(account, ICP)
