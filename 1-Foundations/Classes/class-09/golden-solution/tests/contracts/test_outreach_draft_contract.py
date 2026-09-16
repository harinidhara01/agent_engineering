import pytest
from pydantic import ValidationError

from widgetware_sdr.contracts.outreach_draft import OutreachDraft


def test_a_well_formed_draft_validates() -> None:
    draft = OutreachDraft(
        account_id="acme-001",
        message="Hi — following up on your digital-transformation initiative...",
        used_claims=["acme-001-ev-001"],
    )
    assert draft.requested_action == "send_outreach"


def test_draft_has_no_field_that_could_mean_it_was_sent() -> None:
    """A structural check, not just a naming convention: this contract
    cannot represent "sent" because no such field exists on it.
    """
    field_names = set(OutreachDraft.model_fields.keys())
    assert "sent" not in field_names
    assert "sent_at" not in field_names
    assert "delivery_status" not in field_names


def test_extra_fields_are_rejected() -> None:
    with pytest.raises(ValidationError):
        OutreachDraft(account_id="acme-001", message="Hi.", sent=True)
