"""Context builder module for the WidgetWare SDR package."""

import copy
from pathlib import Path
from typing import Any

import yaml

from widgetware_sdr.instructions import get_system_instructions


def _load_yaml(file_path: Path) -> dict[str, Any]:
    """Load and parse a YAML file, raising a clear error if missing or invalid."""
    if not file_path.exists():
        raise FileNotFoundError(f"Required configuration file missing: {file_path}")
    
    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
        
    if data is None:
        raise ValueError(f"Configuration file is empty: {file_path}")
        
    return data


def build_context(
    account: dict[str, Any],
    objective: str,
    evidence: list[dict[str, Any]],
    state: dict[str, Any] | None = None,
    config_dir: str | Path | None = None,
) -> dict[str, Any]:
    """Assemble the 5-layer context package for WidgetWare SDR analysis.

    Args:
        account: Target account data dictionary (untrusted task data).
        objective: Objective string for the task.
        evidence: List of evidence dictionaries with provenance.
        state: Workflow execution state dictionary (defaults to empty dict).
        config_dir: Directory containing YAML configuration files.

    Returns:
        Structured context dictionary containing the 5 context layers:
        - system_instructions
        - business_context
        - task_context
        - retrieved_evidence
        - state
    """
    if config_dir is None:
        # Default to looking in 'config' in current working directory or relative to package
        cwd_config = Path.cwd() / "config"
        pkg_config = Path(__file__).resolve().parent.parent.parent / "config"
        if cwd_config.exists():
            base_config_dir = cwd_config
        else:
            base_config_dir = pkg_config
    else:
        base_config_dir = Path(config_dir)

    products = _load_yaml(base_config_dir / "products.yaml")
    icp = _load_yaml(base_config_dir / "icp.yaml")
    policies = _load_yaml(base_config_dir / "policies.yaml")

    # Deepcopy inputs to ensure immutability of parameters passed by caller
    account_copy = copy.deepcopy(account)
    evidence_copy = copy.deepcopy(evidence)
    state_copy = copy.deepcopy(state) if state is not None else {}

    return {
        "system_instructions": get_system_instructions(),
        "business_context": {
            "products": products,
            "icp": icp,
            "policies": policies,
        },
        "task_context": {
            "account": account_copy,
            "objective": objective,
        },
        "retrieved_evidence": evidence_copy,
        "state": state_copy,
    }
