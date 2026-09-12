# Class 8 Slides — Multi-Agent Workflow and Human Approval

12 slides, ~2 minutes of speaking notes each, for the 0:30–0:55 segment.

---

## Slide 1 — Current WidgetWare state: qualification and research, uncoordinated

**On slide:** Two real capabilities. No connection between them.

**Say:** "You can research an account. You can qualify one. Nothing today makes those the same run, and nothing decides what happens after either one finishes."

---

## Slide 2 — Today's dependency

**On slide:** `ResearchBrief` and `QualificationResult` become handoff payloads between agents, not standalone outputs.

**Say:** "Every contract we've built was quietly preparing for this class. Today they finally pass between components instead of just validating in isolation."

---

## Slide 3 — Business objective

**On slide:** One coordinated workflow, ending in a human approval gate, never an autonomous send.

**Say:** "The end state today is a person looking at a screen and clicking approve, reject, or revise. That's the whole objective, stated plainly."

---

## Slide 4 — Core concept: why multiple agents (§9.1)

**On slide:** Research Agent, Qualification Agent, Evidence Reviewer, Drafting Agent — each with one responsibility.

**Say:** "A single agent doing all four jobs would have crowded instructions, contradictory context, and no way to isolate which part failed. Splitting responsibility is what makes each part independently testable — which we've been doing since Class 3."

---

## Slide 5 — Workflow patterns (§9.2); typed handoffs (§9.4)

**On slide:** Sequential for Book 1. Pass contracts, never transcripts.

**Say:** "The Drafting Agent gets the Evidence Reviewer's approved claims — not the conversation that produced them, not the raw research. A narrower handoff is a safer one."

---

## Slide 6 — Architecture: state machine before agent prompt (§9.3)

**On slide:** Ten explicit states, an allowed-transitions table, checked before any agent's own words are trusted.

**Say:** "A model can recommend the next step. Only this table decides whether that recommendation is legal. That line is the whole chapter, really."

---

## Slide 7 — Seven Steps mapping

**On slide:** Orchestrate Workflows — the first chapter mainly about coordination, not capability.

**Say:** "Every earlier chapter built one piece well. Today's chapter is entirely about what happens between pieces."

---

## Slide 8 — Gemini vs. deterministic code

**On slide:** Each agent reasons within its role. Code enforces which state transitions are legal.

**Say:** "None of the four agents know the full state machine. None of them need to. That knowledge belongs entirely to `state_machine.py`."

---

## Slide 9 — Security: human-in-the-loop approval (§9.6)

**On slide:** Approval is a state and a policy decision — not an instruction asking the model to check first.

**Say:** "There's no prompt anywhere that says 'ask the user before sending.' There's no send tool to ask permission for in the first place. That's a stronger guarantee than any instruction could be."

---

## Slide 10 — Today's increment

**On slide:** Research → Qualify → Review → Draft → `AWAITING_APPROVAL`.

**Say:** "Watch that last state name. Not 'sent.' Not 'complete.' `AWAITING_APPROVAL` — because that's genuinely as far as this system is allowed to go on its own."

---

## Slide 11 — Lab architecture: partial failure (§9.7)

**On slide:** A visible state and a next action for every failure — never restart everything.

**Say:** "We're going to kill the workflow mid-run today, on purpose, and confirm the research it already did survives. Losing completed work on a downstream failure is exactly what this section exists to prevent."

---

## Slide 12 — Acceptance criteria

**On slide:** Outreach is based only on Evidence-Reviewer-approved claims. No send tool exists anywhere in this codebase.

**Say:** "We're going to grep the entire repository, live, for anything that could send a message. Finding nothing is the point."
