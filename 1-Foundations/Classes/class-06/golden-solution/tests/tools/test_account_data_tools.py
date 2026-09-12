"""Tool tests, independent of any agent — Book 1 §7.8.

Covers what §7.8's list actually applies to for these three read-only,
local tools: valid input, invalid input, missing record, and
deterministic output shape. Dependency failure, permission failure, and
redaction of prohibited fields don't apply yet — there is no external
dependency, no auth boundary, and no sensitive field in this simple
schema. See KNOWN_FAILURE_CASES.md #1 for why that's a real, not just
theoretical, gap.
"""

from widgetware_sdr.tools.account_data import (
    get_account_profile,
    get_icp_policy,
    get_widgetware_product,
)


def test_get_account_profile_valid_input() -> None:
    result = get_account_profile("acme-001")
    assert result["company_name"] == "Acme Manufacturing"
    assert "error" not in result


def test_get_account_profile_invalid_input() -> None:
    result = get_account_profile("")
    assert result["error_category"] == "invalid_input"


def test_get_account_profile_invalid_input_type() -> None:
    result = get_account_profile(None)  # type: ignore[arg-type]
    assert result["error_category"] == "invalid_input"


def test_get_account_profile_missing_record() -> None:
    result = get_account_profile("does-not-exist-999")
    assert result["error_category"] == "not_found"
    assert "does-not-exist-999" in result["error"]


def test_get_account_profile_deterministic_output_shape() -> None:
    """Same input, same output shape, every call — no randomness, no
    hidden dependency on wall-clock time or call order.
    """
    first = get_account_profile("acme-001")
    second = get_account_profile("acme-001")
    assert first == second


def test_get_widgetware_product_valid_input() -> None:
    result = get_widgetware_product("plant-modernization-suite")
    assert "approved_claims" in result
    assert "error" not in result


def test_get_widgetware_product_missing_record() -> None:
    result = get_widgetware_product("nonexistent-product")
    assert result["error_category"] == "not_found"


def test_get_widgetware_product_invalid_input() -> None:
    result = get_widgetware_product("")
    assert result["error_category"] == "invalid_input"


def test_get_icp_policy_returns_the_real_configured_thresholds() -> None:
    """This tool has no input to validate — it always returns the
    current config, which is itself the point: never a stale or
    hardcoded copy.
    """
    policy = get_icp_policy()
    assert policy["minimum_employee_count"] == 5000
    assert "manufacturing" in policy["preferred_industries"]
