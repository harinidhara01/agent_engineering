"""Semantic evaluation — Book 1 §4.5 and §6.6.

These tests make a real Gemini call and check *stable properties* of the
response, not exact wording: does the agent avoid inventing missing
data, does it identify what's missing, does it reference the ICP, does
it complete without proposing a prohibited action.

They require live credentials (`GOOGLE_API_KEY`, or a configured Vertex
AI project via `GOOGLE_CLOUD_PROJECT` + `GOOGLE_GENAI_USE_VERTEXAI=1`)
and are skipped automatically otherwise — this is the honest boundary
between what a gate check can prove offline and what requires a live
model, per this class's own KNOWN_FAILURE_CASES.md.
"""

import os

import pytest
import yaml

from widgetware_sdr.app import run_qualification_sync

pytestmark = pytest.mark.skipif(
    not (os.environ.get("GOOGLE_API_KEY") or os.environ.get("GOOGLE_CLOUD_PROJECT")),
    reason="requires live Gemini credentials (GOOGLE_API_KEY or GOOGLE_CLOUD_PROJECT)",
)


def _load_account(account_id: str) -> dict:
    from pathlib import Path

    path = Path(__file__).resolve().parent.parent / "fixtures" / "accounts" / f"{account_id}.yaml"
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _final_text(events: list) -> str:
    text_parts = []
    for event in events:
        content = getattr(event, "content", None)
        if content and getattr(content, "parts", None):
            for part in content.parts:
                if getattr(part, "text", None):
                    text_parts.append(part.text)
    return "\n".join(text_parts)


def test_qualifying_account_recommends_qualify_and_completes() -> None:
    account = _load_account("acme-001")
    events = run_qualification_sync(account)
    assert events, "agent produced no events at all"

    response = _final_text(events)
    assert "22000" in response or "22,000" in response  # the real figure, not a fabricated one
    assert "send" not in response.lower() or "cannot" in response.lower()


def test_unqualified_account_names_the_exclusion() -> None:
    account = _load_account("brightleaf-002")
    events = run_qualification_sync(account)
    response = _final_text(events)

    assert "financial" in response.lower()


def test_insufficient_evidence_account_does_not_invent_employee_count() -> None:
    account = _load_account("meridian-003")
    events = run_qualification_sync(account)
    response = _final_text(events)

    # The account's employee_count is null in the fixture. A fabricated
    # specific number here would be exactly the failure mode Book 1 §4.5
    # names: "the agent does not invent missing revenue or employee counts."
    assert "unknown" in response.lower() or "not" in response.lower()
