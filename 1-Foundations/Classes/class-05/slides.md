# Class 5 Slides — Structured Outputs and Agent Contracts

12 slides, ~2 minutes of speaking notes each, for the 0:20–0:45 segment.

---

## Slide 1 — Current WidgetWare state: reasons well, returns prose

**On slide:** Class 4's agent produces a correct, well-reasoned answer — as free-form text.

**Say:** "The reasoning has been solid for two classes now. Today's problem isn't reasoning quality — it's what happens the moment something downstream needs to act on the result."

---

## Slide 2 — Today's dependency

**On slide:** Class 4's Skill-driven agent and its model call don't change.

**Say:** "We're not touching the agent today. We're building a layer that sits after it."

---

## Slide 3 — Business objective

**On slide:** A validated, machine-checkable qualification result, safe to route on.

**Say:** "'Looks qualified' is not the same as 'is safely routable.' Today's output has to be the second thing."

---

## Slide 4 — Core concept: why prose isn't enough (§6.1–6.2)

**On slide:** A downstream system can't safely branch on a sentence that might rephrase itself every call.

**Say:** "String-matching against model prose is exactly the kind of fragile integration that breaks in production the first time the model phrases something slightly differently — with no warning."

---

## Slide 5 — Terminology: schema vs. contract vs. validation (§6.3)

**On slide:** A schema describes shape. A contract adds business invariants. Validation enforces both.

**Say:** "Pydantic gets you the schema almost for free. The business invariants — the actual rules of *this* domain — are what we have to write ourselves."

---

## Slide 6 — Architecture: the four business invariants (§6.4)

**On slide:** `QUALIFIED` needs evidence. `NOT_QUALIFIED` needs exclusions. `NEEDS_RESEARCH` needs missing info. `BLOCKED` needs an error.

**Say:** "Each of these is a rule a human reviewer would apply instinctively — 'you can't say qualified with nothing to back it up.' We're just making the computer enforce it too."

---

## Slide 7 — Seven Steps mapping: Evaluate & Govern

**On slide:** Chapter 6 — the first chapter squarely about making an agent's output trustworthy.

**Say:** "Every step so far has been about getting the agent to do the right thing. This one is about proving it did — mechanically, not by reading its prose and trusting it."

---

## Slide 8 — Gemini vs. deterministic code

**On slide:** The agent still reasons in prose. Parsing, schema validation, and invariant checks are pure deterministic code.

**Say:** "Nothing about today's work touches the model. That's the point — trust in the output comes from code you can read and test, not from a stronger prompt."

---

## Slide 9 — Security: fail-safe design (§6.5)

**On slide:** Malformed output becomes a `BLOCKED` result with the error preserved, never a silent pass-through.

**Say:** "A parser that raises an unhandled exception on bad input takes down the pipeline. A parser that silently accepts bad input is worse — it lies. `BLOCKED`, with the error attached, is the only honest third option."

---

## Slide 10 — Today's increment

**On slide:** `contracts/evidence.py`, `contracts/qualification.py`, `parse_qualification_result()`.

**Say:** "Two small contract files and one function that never throws. That's the whole surface area."

---

## Slide 11 — Lab architecture: one failing-case test per invariant

**On slide:** Four ways to be wrong, one way to be right — each with its own test.

**Say:** "A contract you've only tested on the happy path isn't proven yet. The failing-case tests are where the actual value of writing the invariants down shows up."

---

## Slide 12 — Acceptance criteria: the agent is untouched

**On slide:** `qualification_agent.py` is byte-for-byte unchanged from Class 4.

**Say:** "If you find yourself editing the agent file today, stop — that's a sign the contract layer isn't actually separable from the agent, which defeats today's whole design goal."
