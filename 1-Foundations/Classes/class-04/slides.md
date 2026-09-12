# Class 4 Slides — Skills and Reusable Agent Capabilities

12 slides, ~2 minutes of speaking notes each, for the 0:30–0:55 segment.

---

## Slide 1 — Current WidgetWare state: an agent whose procedure is embedded prose

**On slide:** `qualification_agent.py` works, but its qualification procedure is a Python string constant only it can see.

**Say:** "Last class we got an agent reasoning for the first time. Today we ask: what happens the moment a second agent needs that exact same reasoning?"

---

## Slide 2 — Today's dependency

**On slide:** Class 3's agent boundary and model call don't change — only where the procedure lives.

**Say:** "We are not rebuilding the agent. We're extracting one thing out of it and making it reusable."

---

## Slide 3 — Business objective

**On slide:** A reusable, versioned qualification procedure, usable by more than one agent.

**Say:** "WidgetWare doesn't have one agent forever — it'll have a research agent, a review agent, more. If the qualification logic lives only inside one Python string, none of them can share it."

---

## Slide 4 — Core concept: Skill vs. prompt vs. tool (§5.2–5.3)

**On slide:** A Skill tells the agent *how*; a tool lets it *do*.

**Say:** "A prompt is disposable and specific to one call. A tool reaches outside the agent to take an action. A Skill is neither — it's a packaged, reusable piece of know-how the agent loads into its reasoning."

---

## Slide 5 — Terminology: anatomy of a useful Skill (§5.5)

**On slide:** Identity, inputs, procedure, quality criteria, examples.

**Say:** "A Skill that's just a paragraph of advice isn't a Skill yet — it needs the same discipline a good function signature has: what goes in, what comes out, and how to judge it went well."

---

## Slide 6 — Architecture: progressive disclosure (§5.6)

**On slide:** A concise discovery description first; full detail only when the Skill is actually selected.

**Say:** "If every Skill's full text loaded into every agent's context all the time, you'd drown in tokens before the agent did any real work. Discovery stays cheap; detail loads on demand."

---

## Slide 7 — Seven Steps mapping: Design Agent Capabilities

**On slide:** Chapter 5 — the first chapter primarily about making a capability reusable.

**Say:** "Build the Harness got the agent running. Design Agent Capabilities is about making what it knows how to do something you can hand to the next agent, unchanged."

---

## Slide 8 — Gemini vs. deterministic code

**On slide:** The agent reasons. `skills.py`'s file loading stays deterministic.

**Say:** "Loading a Skill file off disk is boring, deterministic code on purpose — the only place probability belongs is in how the agent applies the procedure once it's loaded."

---

## Slide 9 — Security: versioning and ownership (§5.7)

**On slide:** A Skill is an organizational asset, not an anonymous prompt fragment.

**Say:** "Once qualification logic lives in a file with a name, a version, and an owner, you can review changes to it the same way you'd review a change to a database schema. That was impossible when it was a string buried in `qualification_agent.py`."

---

## Slide 10 — Today's increment

**On slide:** `skills/icp_qualification/`, `skills/evidence_classification/`, `skills.py`.

**Say:** "One Skill extracted from last class's agent. One brand-new Skill. One small loader that both depend on."

---

## Slide 11 — Lab architecture: three worked examples per Skill

**On slide:** One positive, one negative, one ambiguous — per Skill.

**Say:** "A Skill without examples is just instructions. Examples are what let the agent — and future engineers — see the boundary cases, not just the easy ones."

---

## Slide 12 — Acceptance criteria: no leftover logic in the agent

**On slide:** After today, `qualification_agent.py` contains no qualification logic of its own.

**Say:** "If you can still find the reasoning steps typed out in the Python file after this refactor, the extraction isn't done — the agent should only be wiring context, Skill, and model together."
