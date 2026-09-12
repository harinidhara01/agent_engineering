import pytest
from pydantic import ValidationError

from widgetware_sdr.contracts.evidence_review import EvidenceReview


def test_a_well_formed_approved_review_validates() -> None:
    review = EvidenceReview(
        account_id="acme-001",
        approved_claims=["acme-001-ev-001: digital-transformation initiative announced"],
        sources_current=True,
        approved_for_drafting=True,
    )
    assert review.approved_for_drafting is True


def test_approved_for_drafting_with_no_approved_claims_is_rejected() -> None:
    with pytest.raises(ValidationError):
        EvidenceReview(
            account_id="acme-001",
            approved_claims=[],
            sources_current=True,
            approved_for_drafting=True,
        )


def test_not_approved_for_drafting_with_no_claims_is_valid() -> None:
    """A review can legitimately reject everything — that's not an
    error, it's the review doing its job.
    """
    review = EvidenceReview(
        account_id="acme-001",
        approved_claims=[],
        rejected_claims=["unsupported claim about company size"],
        sources_current=False,
        approved_for_drafting=False,
    )
    assert review.approved_for_drafting is False
