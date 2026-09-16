# Class 4 — Skills and Reusable Agent Capabilities

**Manuscript source:** Book 1, Chapter 5 — Skills and Reusable Agent Capabilities
**Seven-Step mapping:** Primary: Design Agent Capabilities / Supporting: Build Context, Build the Harness, Evaluate & Govern
**Golden solution produced:** `class-04/golden-solution/`
**Starting checkpoint:** `class-03/golden-solution/`

## 0:00–0:30 — Homework review, common mistakes, golden solution reveal

- **Review homework:** ask participants to show the boundary-condition test they added (exactly 5,000 employees) and confirm the embedded procedure handled it correctly.
- **Common mistakes to flag:** procedure text that reads well but hides an ambiguity at exactly the threshold; sample account data that drifted slightly from the canonical WidgetWare business brief.
- **Golden solution reveal:** walk `class-03/`'s agent, run it once, and ask: "If a second agent needed this exact same reasoning, what would you have to do right now?" (Copy-paste the string. That's the problem today solves.)

## Slide outline (0:30–0:55)

1. Current WidgetWare state: an agent whose procedure is embedded prose
2. Today's dependency: Class 3's agent boundary and model call don't change — only where the procedure lives
3. Business objective: a reusable, versioned qualification procedure, usable by more than one agent
4. Core concept: Skill vs. prompt vs. tool (§5.2–5.3) — a Skill tells the agent how; a tool lets it do
5. Terminology: anatomy of a useful Skill (§5.5) — identity, inputs, procedure, quality criteria, examples
6. Architecture: progressive disclosure (§5.6) — a concise discovery description, full detail only when selected
7. Seven Steps mapping: Design Agent Capabilities — the first chapter primarily about making a capability reusable
8. Gemini vs. deterministic code: the agent reasons; `skills.py`'s file loading stays deterministic
9. Security: versioning and ownership (§5.7) — a Skill is an organizational asset, not an anonymous prompt fragment
10. Today's increment: `skills/icp_qualification/`, `skills/evidence_classification/`, `skills.py`
11. Lab architecture: three worked examples per Skill — one positive, one negative, one ambiguous
12. Acceptance criteria: the agent file contains no qualification logic of its own afterward

## Kahoot (8 questions)

- Terminology: What is the difference between a Skill and a tool (§5.3)?
- Terminology: What is the difference between a Skill and a workflow (§5.4)?
- Architecture: Why does progressive disclosure (§5.6) matter for context consumption?
- Architecture: Why move the qualification procedure out of the agent's embedded instructions and into a Skill?
- Failure analysis: The agent confidently qualifies an account with clearly insufficient evidence — where's the fix, agent code or Skill procedure?
- Security/governance: What does §5.7 say a Skill needs that "an anonymous prompt fragment" doesn't?
- WidgetWare scenario: A second agent needs the same qualification logic — what does the Skill's reusability buy you here?
- Connecting back: How does §3.5's evidence-policy vocabulary (Class 2) show up inside the Skill's procedure?

## Build together (1:05–1:35)

- `skills/icp_qualification/skill.md`, `examples/{qualified,unqualified,needs_research}.md`, `tests/cases.yaml`
- refactor `qualification_agent.py` to read its procedure from the Skill instead of an embedded instruction block
- add the lightweight **Evidence Classification** Skill (verified fact / derived fact / inference / unknown / conflict)

## Test and diagnose (1:35–1:50)

1. Run the qualified-account scenario test (happy path).
2. Run the uncertain-account test: does the agent still correctly say "insufficient evidence"?
3. Trigger a comparison: run the *pre-refactor* agent (embedded prompt) against a scenario, then the *post-refactor* Skill-driven agent against the same scenario, and diff the reasoning.
4. Inspect the event sequence and assembled instructions — confirm the instruction now contains the Skill's text, loaded, not retyped.
5. Diagnose: is a discrepancy caused by the Skill's procedure being under-specified, or a loading bug in `skills.py`?
6. Apply the smallest fix — usually tightening the Skill's procedure or examples, not the agent's Python code.
7. Re-run all three scenario tests.

## Homework

| Level | Task |
| ----- | ---- |
| **Required** | Qualification agent runs reproducibly against all three scenario accounts, driven entirely by the Skill (no embedded procedure left in Python) |
| **Diagnostic** | The Evidence Classification Skill misclassifies one deliberately ambiguous fact in the provided test case — fix the Skill, not the agent |
| **Extension** | Write a second, independent Skill consumer — a small script that loads `icp_qualification` and prints its procedure, proving the Skill is genuinely reusable outside `qualification_agent.py` |

- **Starting checkpoint:** `class-03/golden-solution/`
- **Files participants may modify:** `skills/`, `src/widgetware_sdr/agents/qualification_agent.py`, `src/widgetware_sdr/skills.py`, `tests/`
- **Expected behavior:** the agent's qualification procedure lives entirely in the Skill; the agent code only wires context, Skill, and model together
- **Tests that must pass:** all three scenario tests, plus the "no embedded procedure" structural test
- **Submission:** local-playground event-sequence printout for one scenario, plus test output
- **Constraints:** no structured/typed output yet (Chapter 6) — the agent's result is still prose at this stage, on purpose; no tools yet (Chapter 7)

## Golden solution: `class-04/`

Adds both Skills and the loader on top of `class-03/`, and refactors the agent to load from them. README notes the Chapter 4 checkpoint's own framing — "it does not yet expose its procedure as a reusable Skill" — and shows this checkpoint closing that gap.

## Bridge to Class 5

Class 5 replaces the agent's prose output with a typed, validated contract — the Skill's procedure still describes the reasoning; Class 5 only changes how the result is captured afterward.
