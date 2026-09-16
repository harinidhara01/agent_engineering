# Class 10 Slides — Loop Engineering with ADK

12 slides, ~2 minutes of speaking notes each, for the 0:20–0:45 segment. This class closes Book 1.

---

## Slide 1 — Current WidgetWare state: proven, but only for one account at a time

**On slide:** Class 9's release gate passes. The workflow is good enough to ship — run once, on request.

**Say:** "We proved it's trustworthy. We haven't yet asked it to do that unattended, at scale, for a hundred accounts overnight."

---

## Slide 2 — Today's dependency

**On slide:** Nothing about `run_workflow` changes today. The loop wraps it, unchanged, exactly as Class 9 left it.

**Say:** "This is the whole ordering argument from last class, paying off. We evaluated first. Now, and only now, we automate."

---

## Slide 3 — Business objective

**On slide:** Run the same proven workflow unattended, across a queue, safely and within stated budgets.

**Say:** "Same trust bar as a person running it by hand — just without the person."

---

## Slide 4 — Core concept: a loop is not `max_iterations` alone (§11.4)

**On slide:** Seven things §11.4 says `max_iterations` doesn't give you: work selection, durable state, verification, budgets, decisions, reporting, and a stop reason.

**Say:** "The obvious, minimal version of a loop — just repeat until a counter runs out — is not the real thing. Today builds the real thing."

---

## Slide 5 — Terminology: the inner loop vs. the outer loop (§11.2–11.3)

**On slide:** The inner ADK reasoning loop is one agent's own observe-reason-act cycle within a single call. The outer loop this chapter adds decides what to work on next, across many separate invocations.

**Say:** "Two completely different things share the word 'loop.' Keep them distinct in your head, because we're building the outer one today."

---

## Slide 6 — Architecture: the five-way decision (§11.8)

**On slide:** CONTINUE, RETRY, STOP, DEFER, ESCALATE.

**Say:** "Every account, every iteration, lands on exactly one of these five. If your code has a sixth implicit outcome — silently doing nothing — that's a bug hiding as a feature."

---

## Slide 7 — Seven Steps mapping: Engineer Loops

**On slide:** Chapter 11 — the final primary step of Book 1.

**Say:** "We've built a harness, capabilities, a validated workflow, and proof it's good enough to ship. The last piece is making it run without someone watching."

---

## Slide 8 — Gemini vs. deterministic code

**On slide:** The workflow's reasoning is unchanged. Everything new today — budget checks, decisions, queue selection — is deterministic.

**Say:** "Not one new model call gets added today. The loop is entirely engineering around a model call we already trust."

---

## Slide 9 — Security: authority doesn't change inside a loop (§11.10)

**On slide:** The approval table from Class 8, unchanged, still enforced per account.

**Say:** "An account processed at 3am inside an unattended batch gets exactly the same approval scrutiny as one processed live, on request, with a person watching. Unattended is not the same as unsupervised."

---

## Slide 10 — Today's increment

**On slide:** `loop/budget.py`, `loop/decision.py`, `loop/account_queue.py`, `loop/run_report.py`, `loop/batch_runner.py`, plus two new workflow states.

**Say:** "Five small files and two new states in a table we already built. That's the entire engineered loop."

---

## Slide 11 — Lab architecture: verification before advancing (§11.7)

**On slide:** Trust only the state the workflow actually reached — never an agent's own unverified claim about what happened.

**Say:** "Before the loop decides what's next for an account, it checks, in code, what state that account is actually in. It never just believes a summary."

---

## Slide 12 — Acceptance criteria: a loop that can explain itself

**On slide:** The loop stops for a reason it can name, every time.

**Say:** "By the end of today, ask the batch loop why it stopped, and it will actually tell you — not 'something went wrong,' a specific, named reason. That's Book 1, done."
