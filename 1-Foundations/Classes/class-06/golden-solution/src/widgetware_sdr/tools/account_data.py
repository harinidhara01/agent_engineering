"""Internal data tools — Book 1, Chapter 7.

Each tool has a single clear responsibility, a typed and validated
input, a compact and sourced output, and never fabricates a result for
data it cannot find. Book 1 keeps these read-only and local — no
external network call and no write capability exist anywhere in this
codebase.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

DATA_DIR = Path(__file__).resolve().parent.parent.parent.parent / "data" / "sample_accounts"
CONFIG_DIR = Path(__file__).resolve().parent.parent.parent.parent / "config"


def get_account_profile(account_id: str) -> dict[str, Any]:
    """Retrieve a WidgetWare account profile by its exact account_id.

    Use this to look up a specific, already-known account's industry,
    employee count, region, and known challenges. Do not use this to
    search for accounts by company name — it requires the exact
    account_id and will not fuzzy-match.

    Args:
        account_id: The account's unique identifier, e.g. "acme-001".

    Returns:
        A dict of the account's normalized fields on success, or a dict
        with "error" and "error_category" keys on failure. Never
        fabricates a profile for an account_id that does not exist.
    """
    if not isinstance(account_id, str) or not account_id.strip():
        return {"error": "account_id must be a non-empty string", "error_category": "invalid_input"}

    path = DATA_DIR / f"{account_id}.yaml"
    if not path.exists():
        return {
            "error": f"no account found for account_id={account_id!r}",
            "error_category": "not_found",
        }

    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_widgetware_product(product_id: str) -> dict[str, Any]:
    """Retrieve one WidgetWare product's approved facts and claims.

    Use this before referencing any product capability in a
    qualification rationale or draft — only claims listed here are
    approved for use.

    Args:
        product_id: The product's identifier, e.g. "plant-modernization-suite".

    Returns:
        A dict with the product's summary and approved/unapproved
        claims on success, or an error dict on failure.
    """
    if not isinstance(product_id, str) or not product_id.strip():
        return {"error": "product_id must be a non-empty string", "error_category": "invalid_input"}

    products = _load_products()
    for product in products:
        if product["product_id"] == product_id:
            return product
    return {
        "error": f"no product found for product_id={product_id!r}",
        "error_category": "not_found",
    }


def get_icp_policy() -> dict[str, Any]:
    """Retrieve WidgetWare's current ideal-customer-profile configuration.

    Use this to obtain the authoritative, current ICP thresholds rather
    than relying on any value stated earlier in a conversation — the
    configuration file is always the source of truth.

    Returns:
        A dict of the current ICP configuration.
    """
    path = CONFIG_DIR / "icp.yaml"
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _load_products() -> list[dict[str, Any]]:
    path = CONFIG_DIR / "products.yaml"
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)["products"]
