"""Tests that verify the checkpoint itself, not WidgetWare business logic.

There is no qualification agent yet, so there is nothing to test about
qualification. What *does* exist at this checkpoint is a repository with a
specific, promised shape — a harness, a charter, and a boundary — and that
shape is exactly what these tests check.

These tests deliberately avoid adding a YAML-parsing dependency: PyYAML is
introduced starting Class 2 (Book 1, Chapter 3), and pulling it in a class
early would misrepresent when that dependency actually enters the project.
The fixture files here are simple enough that a small scalar-field reader
is sufficient and honest about what it does.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

REQUIRED_DOCS = [
    "README.md",
    "SPEC.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "KNOWN_FAILURE_CASES.md",
    "docs/widgetware-business-brief.md",
    "docs/acceptance-criteria.md",
    "docs/architecture.md",
    "docs/architecture-decisions/0001-bounded-autonomy.md",
    "docs/architecture-decisions/0002-no-outbound-send.md",
    "docs/architecture-decisions/0003-repository-harness.md",
]

REQUIRED_AGENT_FILES = [
    ".agents/rules/engineering.md",
    ".agents/rules/security.md",
    ".agents/workflows/baseline-check.md",
]

ALLOWED_QUALIFICATION_DIRECTIONS = {"QUALIFIED", "NOT_QUALIFIED", "NEEDS_RESEARCH"}

FORBIDDEN_IMPORT_PATTERNS = [
    re.compile(r"^\s*import\s+google\.generativeai", re.MULTILINE),
    re.compile(r"^\s*from\s+google\.generativeai", re.MULTILINE),
    re.compile(r"^\s*import\s+google\.adk", re.MULTILINE),
    re.compile(r"^\s*from\s+google\.adk", re.MULTILINE),
    re.compile(r"^\s*import\s+vertexai", re.MULTILINE),
    re.compile(r"^\s*from\s+vertexai", re.MULTILINE),
]

SEND_CAPABLE_NAME_PATTERN = re.compile(
    r"\b(def\s+send_\w*|smtplib|sendgrid|twilio|send_email|send_message)\b", re.IGNORECASE
)

# Bounded, honest credential-shape check: known real-key prefixes, not a
# general secret scanner. This catches an accidentally pasted real key; it
# is not a substitute for a dedicated secret-scanning tool.
CREDENTIAL_LIKE_PATTERNS = [
    re.compile(r"AIza[0-9A-Za-z_-]{35}"),  # Google API key shape
    re.compile(r"sk-[A-Za-z0-9]{20,}"),  # common vendor secret-key shape
    re.compile(r"AKIA[0-9A-Z]{16}"),  # AWS access key ID shape
]


def _read_scalar_field(path: Path, key: str) -> str:
    """Extract a simple ``key: value`` scalar from a small flat YAML file."""
    pattern = re.compile(rf"^{re.escape(key)}:\s*(\S.*)$")
    for line in path.read_text(encoding="utf-8").splitlines():
        match = pattern.match(line.strip())
        if match:
            return match.group(1).strip()
    raise AssertionError(f"No scalar field {key!r} found in {path}")


def _python_files(*dirs: Path) -> list[Path]:
    files: list[Path] = []
    for d in dirs:
        if d.exists():
            files.extend(sorted(d.rglob("*.py")))
    return files


def test_package_is_importable() -> None:
    import widgetware_sdr  # noqa: PLC0415

    assert widgetware_sdr.__version__


def test_health_check_is_deterministic_across_calls() -> None:
    from widgetware_sdr.health import health_check  # noqa: PLC0415

    assert health_check() == health_check()


def test_required_documentation_files_exist() -> None:
    missing = [doc for doc in REQUIRED_DOCS if not (REPO_ROOT / doc).is_file()]
    assert not missing, f"Missing required documentation: {missing}"


def test_required_agent_rules_and_workflows_exist() -> None:
    missing = [f for f in REQUIRED_AGENT_FILES if not (REPO_ROOT / f).is_file()]
    assert not missing, f"Missing required .agents/ files: {missing}"


def test_env_example_exists() -> None:
    assert (REPO_ROOT / ".env.example").is_file()


def test_real_env_file_is_not_part_of_the_checkpoint() -> None:
    assert not (REPO_ROOT / ".env").exists(), (
        ".env must never be committed — only .env.example belongs in the repository."
    )


def test_gitignore_excludes_env_and_generated_artifacts() -> None:
    gitignore = (REPO_ROOT / ".gitignore").read_text(encoding="utf-8")
    required_entries = [".env", ".venv", "__pycache__", ".pytest_cache"]
    missing = [entry for entry in required_entries if entry not in gitignore]
    assert not missing, f".gitignore is missing entries for: {missing}"


def test_no_source_file_imports_gemini_or_adk_yet() -> None:
    offending: list[str] = []
    for py_file in _python_files(REPO_ROOT / "src"):
        text = py_file.read_text(encoding="utf-8")
        for pattern in FORBIDDEN_IMPORT_PATTERNS:
            if pattern.search(text):
                offending.append(str(py_file.relative_to(REPO_ROOT)))
                break
    assert not offending, f"No Gemini or ADK model call belongs in this checkpoint yet: {offending}"


def test_no_send_capable_function_or_outbound_tool_exists() -> None:
    offending: list[str] = []
    for py_file in _python_files(REPO_ROOT / "src"):
        if SEND_CAPABLE_NAME_PATTERN.search(py_file.read_text(encoding="utf-8")):
            offending.append(str(py_file.relative_to(REPO_ROOT)))
    assert not offending, f"No send-capable code belongs in Book 1: {offending}"


def test_no_committed_file_contains_an_obvious_credential() -> None:
    scan_dirs = [
        REPO_ROOT / "src",
        REPO_ROOT / "config",
        REPO_ROOT / "docs",
        REPO_ROOT / "tests",
    ]
    scan_files = list(_python_files(*scan_dirs)) + [REPO_ROOT / ".env.example"]
    offending: list[str] = []
    for f in scan_files:
        if not f.is_file():
            continue
        text = f.read_text(encoding="utf-8")
        if any(pattern.search(text) for pattern in CREDENTIAL_LIKE_PATTERNS):
            offending.append(str(f.relative_to(REPO_ROOT)))
    assert not offending, f"Possible committed credential in: {offending}"


def test_scripts_check_is_executable() -> None:
    check_script = REPO_ROOT / "scripts" / "check.sh"
    assert check_script.is_file()
    assert check_script.stat().st_mode & 0o111, "scripts/check.sh must be executable"


def test_every_scenario_has_a_matching_account_and_expected_fixture() -> None:
    scenarios_dir = REPO_ROOT / "tests" / "scenarios"
    accounts_dir = REPO_ROOT / "tests" / "fixtures" / "accounts"
    expected_dir = REPO_ROOT / "tests" / "fixtures" / "expected"

    scenario_files = sorted(scenarios_dir.glob("*.md"))
    assert len(scenario_files) == 3, (
        f"Expected exactly three scenarios, found {len(scenario_files)}"
    )

    account_ids = {p.stem for p in accounts_dir.glob("*.yaml")}
    expected_ids = {p.stem for p in expected_dir.glob("*.yaml")}
    assert account_ids == expected_ids, (
        f"Account and expected fixtures must match by id: {account_ids} != {expected_ids}"
    )
    assert len(account_ids) == 3


def test_every_expected_fixture_references_its_own_account_id() -> None:
    accounts_dir = REPO_ROOT / "tests" / "fixtures" / "accounts"
    expected_dir = REPO_ROOT / "tests" / "fixtures" / "expected"

    for expected_path in sorted(expected_dir.glob("*.yaml")):
        account_path = accounts_dir / expected_path.name
        assert account_path.is_file(), f"No matching account fixture for {expected_path.name}"

        account_id_in_account = _read_scalar_field(account_path, "account_id")
        account_id_in_expected = _read_scalar_field(expected_path, "account_id")
        assert account_id_in_account == account_id_in_expected == expected_path.stem


def test_expected_qualification_direction_is_an_allowed_value() -> None:
    expected_dir = REPO_ROOT / "tests" / "fixtures" / "expected"
    for expected_path in sorted(expected_dir.glob("*.yaml")):
        direction = _read_scalar_field(expected_path, "expected_qualification_direction")
        assert direction in ALLOWED_QUALIFICATION_DIRECTIONS, (
            f"{expected_path.name}: {direction!r} is not one of "
            f"{sorted(ALLOWED_QUALIFICATION_DIRECTIONS)}"
        )


def test_expected_fixtures_cover_all_three_qualification_directions() -> None:
    expected_dir = REPO_ROOT / "tests" / "fixtures" / "expected"
    directions = {
        _read_scalar_field(p, "expected_qualification_direction")
        for p in expected_dir.glob("*.yaml")
    }
    assert directions == ALLOWED_QUALIFICATION_DIRECTIONS
