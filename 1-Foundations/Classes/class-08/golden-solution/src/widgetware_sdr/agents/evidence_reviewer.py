"""The Evidence Reviewer — Book 1, Chapter 9 (§9.5).

Verifies that decisive qualification claims have citations, sources are
current, contradictions are surfaced, and only approved facts move
forward to drafting. Produces an `EvidenceReview` — the Outreach
Drafting Agent will see nothing except this review's approved claims,
never the raw research brief.
"""

from __future__ import annotations

from google.adk.agents import Agent

from widgetware_sdr.instructions import SYSTEM_INSTRUCTIONS, get_model_id

REVIEWER_INSTRUCTIONS = """\
=== EVIDENCE REVIEW RULES ===

You will be given a ResearchBrief and a QualificationResult. Verify:

- every decisive claim in the qualification has a citation in the
  research brief's evidence;
- sources are current enough to support the claim being made;
- any conflicts in the research brief are surfaced, never silently
  resolved by picking one value;
- unsupported claims are removed from what gets approved; and
- remaining uncertainty is disclosed, not hidden.

Produce an EvidenceReview. Do not independently browse for more
persuasive facts — your job is to check what was found, not to look for
more of it. That would bypass the point of having a review step at all.
"""


def build_agent_instruction() -> str:
    return "\n\n".join([SYSTEM_INSTRUCTIONS.strip(), REVIEWER_INSTRUCTIONS.strip()])


def create_evidence_reviewer_agent() -> Agent:
    return Agent(
        name="evidence_reviewer",
        model=get_model_id(),
        description=(
            "Verifies qualification claims are cited, current, and free of "
            "unsurfaced contradictions before drafting proceeds."
        ),
        instruction=build_agent_instruction(),
    )
