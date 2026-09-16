# Class 6 Slides — Tool Engineering

12 slides, ~2 minutes of speaking notes each, for the 0:20–0:45 segment.

---

## Slide 1 — Current WidgetWare state: validated, but blind

**On slide:** Class 5's agent produces a schema-valid `QualificationResult` — built entirely from whatever facts the caller handed it.

**Say:** "Print a valid result right now and ask: every fact in here, where did it actually come from? The honest answer is 'wherever the caller happened to put it.' The agent has no way to go look anything up itself."

---

## Slide 2 — Today's dependency

**On slide:** Class 5's contracts don't change structurally — tool-retrieved facts just start giving `evidence_refs` something real to point at.

**Say:** "We're not touching `QualificationResult`'s shape today. We're finally giving the agent a way to earn the evidence it claims to have."

---

## Slide 3 — Business objective

**On slide:** An agent that retrieves its own facts instead of trusting whatever it's handed.

**Say:** "This is the difference between an agent that reports what it was told and one that can actually go check."

---

## Slide 4 — Core concept: a tool lets the agent do something outside the model (§7.1)

**On slide:** A Skill tells the agent how. A tool lets it reach outside itself and act.

**Say:** "We named this distinction back in Class 4 and deliberately didn't build a tool yet. Today's the day that other half of the distinction becomes real."

---

## Slide 5 — Terminology: tool descriptions are part of control (§7.2)

**On slide:** The model selects tools by name and description alone — not by reading the implementation.

**Say:** "A vague tool description leads to misuse regardless of how correct the underlying code is. Write the docstring like you're briefing someone who will never see the function body."

---

## Slide 6 — Architecture: three narrow, read-only tools (§7.3)

**On slide:** `get_account_profile`, `get_widgetware_product`, `get_icp_policy` — each does exactly one lookup, nothing else.

**Say:** "Narrow on purpose. A tool that does five things is five ways for the model to misuse it."

---

## Slide 7 — Seven Steps mapping: Design Agent Capabilities continues

**On slide:** Chapter 5 gave the agent a Skill. Chapter 7 gives it a tool — the same step, from the opposite direction.

**Say:** "A Skill shapes what the model knows how to do. A tool shapes what it can reach outside itself. Both are capability engineering."

---

## Slide 8 — Gemini vs. deterministic code

**On slide:** The model decides *when* to call a tool. `calculate_fit_score()` is pure arithmetic and is never exposed as a callable tool at all.

**Say:** "Not everything that touches account data needs to go through the model. A fixed formula belongs in application code, called directly — that's a design decision, not a limitation."

---

## Slide 9 — Security: least privilege for tools (§7.5)

**On slide:** A read-only lookup should never hold write-capable credentials, even if the platform account technically could.

**Say:** "Ask yourselves: what's the actual damage ceiling if one of these three tools were compromised today? For a well-scoped read-only tool, the honest answer should be small."

---

## Slide 10 — Today's increment

**On slide:** `tools/account_data.py`, `tools/fit_score.py`, agent updated with `tools=[...]`.

**Say:** "Three read functions, one arithmetic helper, and one new instruction line telling the model to use them instead of assuming."

---

## Slide 11 — Lab architecture: tool testing without the agent (§7.8)

**On slide:** Valid input, invalid input, missing record, deterministic output shape — tested completely independent of any model call.

**Say:** "We test these tools with zero API calls today, on purpose — so a tool bug and a reasoning bug never get confused with each other."

---

## Slide 12 — Acceptance criteria: real, traceable evidence

**On slide:** Every decisive claim in a qualification result carries an evidence reference traceable to an actual tool call.

**Say:** "If you can point at an `evidence_refs` entry and can't show which tool call produced it, the extraction isn't finished yet — that traceability is the whole payoff of today's work."
