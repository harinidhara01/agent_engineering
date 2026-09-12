# Class 1 Slides — Agent Engineering Foundations and the Antigravity Repository Harness

12 slides, ~2 minutes of speaking notes each, for the 0:30–0:55 segment. (Class 1 also uses its own opening in place of the standard 0:00–0:30 — see `README.md` for that timing.)

---

## Slide 1 — What this course builds, end to end

**On slide:** A ten-class arc. Class 1 → a runnable charter and harness. Class 10 → a bounded, unattended batch loop wrapping a proven workflow.

**Say:** "Everything we build in the next ten classes is one running system — WidgetWare SDR Lab. Today is unusual: we're covering two chapters' worth of ground, because a charter you can't run is a weaker starting point than a charter paired with a workspace that proves it's real."

---

## Slide 2 — A model is a capability, not a system (§1.1); the autonomy spectrum (§1.3)

**On slide:** "A language model predicts and generates language. It does not define responsibility, permission, persistence, or correctness." Seven autonomy levels, Answer-only through Open-ended. WidgetWare stops at level 4: Prepare.

**Say:** "Gemini can summarize, classify, infer, and draft. None of that makes it trustworthy on its own — that's everything we build for the rest of the course. And WidgetWare will research, qualify, and draft entirely on its own, but outbound communication always stops at a human. That boundary doesn't move for the rest of Book 1."

---

## Slide 3 — Probabilistic reasoning inside deterministic boundaries (§1.4)

**On slide:** "Let the model interpret, synthesize, draft. Let software validate, authorize, persist, route, enforce."

**Say:** "This one sentence is the entire book. Every class from here forward is really just this pattern applied to a new part of the system — including today's harness, which is itself an example: Antigravity reasons about how to implement a task, but the repository's own rules fix what's allowed."

---

## Slide 4 — Introducing WidgetWare (§1.5); initial system boundary (§1.6)

**On slide:** WidgetWare sells software that helps manufacturing and industrial-automation companies modernize plant operations. In scope: research, qualify, draft, request approval. Out of scope: autonomous prospecting, sending messages, modifying CRM without approval, inventing facts.

**Say:** "This is our case study for the entire course. Read the out-of-scope list out loud — every one of these is a plausible thing an eager engineer might add 'to save the SDR a click.' This class exists so nobody adds it by accident, today or in Class 8 when the workflow is complete."

---

## Slide 5 — Acceptance criteria written before implementation (§1.7)

**On slide:** Six criteria, each independently testable — schema conformance, evidence-or-inference, no drafting on insufficient evidence, no autonomous send, explainability, usable on representative accounts.

**Say:** "None of these can be satisfied by 'the response looks good.' You'll draft your own version of these in a few minutes, before I show you the reference — I want you to have an opinion about what success means before you've written a line of code."

---

## Slide 6 — Today's increment, part one: the charter

**On slide:** `README.md`, `SPEC.md`, `docs/widgetware-business-brief.md`, `docs/acceptance-criteria.md`, `tests/scenarios/`.

**Say:** "Five files. This part alone used to be the entire first class. It's still real work — but today it's the first half of the class, not all of it."

---

## Slide 7 — Bridge: a charter nobody can run is a weaker checkpoint

**On slide:** "Frame the Use Case is a discipline independent of implementation technology — but proving you did it shouldn't require trusting prose alone."

**Say:** "Everything after this slide used to be an entire separate class. We're folding it in today because the alternative — leaving Class 1 with zero runnable code — meant the course's very first checkpoint was the one thing nobody could verify with a test."

---

## Slide 8 — Core concept: the harness is part of the system (§2.1)

**On slide:** IDE, repo structure, instructions, dependency management, secrets handling, code-quality checks, tests, permissions, review practice.

**Say:** "None of this is scaffolding you throw away later. A strong harness makes both you and Antigravity perform better, because it makes expectations explicit — starting today, not starting 'once we have real code.'"

---

## Slide 9 — Antigravity as engineering partner; README vs. SPEC (§2.2, §2.4); repository structure (§2.3)

**On slide:** The eight-step disciplined cycle: state objective → provide spec → ask for plan → review → permit bounded implementation → inspect diff → run tests → accept/revise/revert.

**Say:** "`README.md` is for people. `SPEC.md` is for the implementation. Antigravity should be handed the spec, not asked to guess your intent from a README — and we're about to watch what happens when we skip that discipline on purpose."

---

## Slide 10 — Security: trust and permissions for a development agent (§2.7)

**On slide:** Least privilege for a *development* agent: review shell commands, restrict production credentials, use `.env.example`, isolate experiments, inspect dependency additions.

**Say:** "'The development agent is a powerful collaborator, not an unquestioned authority.' That line applies before anything sensitive exists to protect — which is exactly our situation right now, with zero real secrets and zero production access."

---

## Slide 11 — Today's increment, part two: the harness

**On slide:** `pyproject.toml`, installable `widgetware_sdr` package, health check, `.env.example`, `.agents/`, and one command — `./scripts/check.sh` — that verifies the environment, then formats, lints, type-checks, and tests everything.

**Say:** "By the end of today, that one command actually runs, and actually passes. That's the whole difference this merged class is trying to make."

---

## Slide 12 — Acceptance criteria, reprised

**On slide:** Every Section A criterion in `docs/acceptance-criteria.md` — the criteria this checkpoint can actually prove today — is checked by `./scripts/check.sh` by the end of this class.

**Say:** "Section B is the finished product's criteria — schema conformance, evidence citation, the rest. We're not there yet, and the document says so honestly. Section A is what today is actually held to, and today, for the first time in this course, that's not just a promise."
