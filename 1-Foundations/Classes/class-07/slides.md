# Class 7 Slides — MCP and Evidence-Backed Research

12 slides, ~2 minutes of speaking notes each, for the 0:30–0:55 segment.

---

## Slide 1 — Current WidgetWare state: trusted internal tools, no external research yet

**On slide:** Three read-only tools, all pointed at WidgetWare's own data.

**Say:** "Every fact the agent has touched so far came from us. Today it looks outside for the first time — and outside data doesn't get to be trusted just because it sounds authoritative."

---

## Slide 2 — Today's dependency

**On slide:** `EvidenceItem` (Class 6) gets its first real external content to hold.

**Say:** "We built the shape of an evidence item two classes ago. Today it finally holds something we didn't already know."

---

## Slide 3 — Business objective

**On slide:** A reproducible, cited account-research brief.

**Say:** "Reproducible and cited — same two words that mattered in Class 3, now applied to a whole pipeline instead of one agent's reasoning."

---

## Slide 4 — Core concept: research is not one model call (§8.1)

**On slide:** Questions → discovery → retrieval → extraction → assessment → contradiction detection → synthesis → citation.

**Say:** "A single model call that says 'go research this company' hides seven distinct failure points behind one opaque step. Today we build a pipeline, not a call."

---

## Slide 5 — Function tools versus MCP (§8.5)

**On slide:** Function tool when the integration is application-specific and narrow; MCP when a standardized server already exists and multiple clients need it.

**Say:** "We're using a function tool today, deliberately — a local mock source. That's the honest choice for this course; the decision framework is what actually matters, not which one we happened to pick."

---

## Slide 6 — Architecture: the evidence ledger (§8.7)

**On slide:** `ResearchBrief`: evidence_items[], claims[], conflicts[], unknowns[], summary, recommended_next_step.

**Say:** "Notice `conflicts[]` sits right next to `claims[]`, not hidden in a log somewhere. Disagreement between sources is a first-class citizen of this structure, not an edge case."

---

## Slide 7 — Seven Steps mapping

**On slide:** Still Design Agent Capabilities.

**Say:** "Research is a capability, engineered with the same rigor as a tool — narrow responsibility, typed output, tested independently."

---

## Slide 8 — Gemini vs. deterministic code

**On slide:** The model may assist at several research stages; deterministic validation rejects any uncited material claim regardless.

**Say:** "Even if the model is genuinely excellent at synthesis, the citation requirement is enforced by code, every time, no exceptions for a confident-sounding answer."

---

## Slide 9 — Security: retrieved content is untrusted data (§8.6)

**On slide:** Isolate, label, extract only task-relevant evidence, never execute instructions found in content.

**Say:** "This is the same discipline from Class 2's account notes, now applied to something that looks more credible because it claims to come from 'TradePress Manufacturing Weekly.' A source that sounds professional is not automatically trustworthy."

---

## Slide 10 — Today's increment

**On slide:** `search_public_records`, `research.py`'s deterministic pipeline, `research_agent.py`.

**Say:** "One tool, one pipeline, one agent. Everything in the pipeline is testable without a model. Only the agent's synthesis needs one."

---

## Slide 11 — Lab architecture: freshness and contradictions (§8.3, §8.4)

**On slide:** A stale source isn't automatically wrong, but it needs to be flagged. A conflict isn't resolved by convenience.

**Say:** "We have a genuinely stale source in our mock data — a 2023 employee count next to a 2026 one. Today's pipeline surfaces that as a conflict, not a coincidence to shrug off."

---

## Slide 12 — Acceptance criteria

**On slide:** Insufficient evidence stops the workflow — it does not produce a confident guess.

**Say:** "We'll run the pipeline against an account with zero mock evidence today and watch it say so honestly, rather than inventing something plausible."
