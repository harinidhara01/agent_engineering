"""The Outreach Drafting Agent — Book 1, Chapter 9 (§9.4).

Consumes only the Evidence Reviewer's approved claims — never the raw
research brief, never anything the reviewer rejected. This is enforced
structurally by what this agent is given as input, not by asking the
model to please only use approved facts.

Produces a draft. Nothing in this codebase can send it anywhere.
"""

from __future__ import annotations

from google.adk.agents import Agent

from widgetware_sdr.instructions import SYSTEM_INSTRUCTIONS, get_model_id

DRAFTING_INSTRUCTIONS = """\
=== DRAFTING RULES ===

You will be given only a list of approved claims — facts the Evidence
Reviewer has already verified and cleared for use. Draft a short
outreach message using only these claims. Do not introduce any fact,
statistic, or claim that is not in the approved list, even if it would
make the message more persuasive.

You are drafting a message for human review, not sending one. State any
remaining risk or uncertainty as a flag alongside the draft.
"""


def build_agent_instruction() -> str:
    return "\n\n".join([SYSTEM_INSTRUCTIONS.strip(), DRAFTING_INSTRUCTIONS.strip()])


def create_drafting_agent() -> Agent:
    return Agent(
        name="drafting_agent",
        model=get_model_id(),
        description=(
            "Drafts outreach messages using only pre-approved claims. "
            "Never sends anything — no send-capable tool exists."
        ),
        instruction=build_agent_instruction(),
    )
