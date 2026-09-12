# Class 2 Slides — Gemini Context and Instruction Architecture

12 slides, ~2 minutes of speaking notes each, for the 0:30–0:55 segment.

---

## Slide 1 — Current WidgetWare state: a runnable, empty, well-governed workspace

**On slide:** `./scripts/check.sh` passes. Zero business logic exists.

**Say:** "We have a workspace we can trust. Today we build the thing every future agent will actually reason over — and we still won't call a model. That's on purpose."

---

## Slide 2 — Today's dependency

**On slide:** No agent gets built in Class 3 without a real context architecture first.

**Say:** "If you skip today and go straight to 'give the agent a big prompt,' every later chapter — evidence, tools, workflows — inherits that mess. This is the highest-leverage class in Book 1 for exactly that reason."

---

## Slide 3 — Business objective

**On slide:** Separate stable policy from task data from retrieved evidence.

**Say:** "Not 'write a good prompt.' Build an architecture with layers, so each layer can be tested, versioned, and reasoned about independently."

---

## Slide 4 — Core concept: model choice is an architectural decision (§3.1)

**On slide:** One question: "Which model provides sufficient quality for this task under the required latency and cost constraints?"

**Say:** "Not 'which model is best' — that question never has a stable answer. Today we centralize model selection in one function so this question can actually be revisited later, in Class 9, with real evaluation data."

---

## Slide 5 — Layers of context (§3.2)

**On slide:** System instructions, business context, task context, retrieved evidence, state — five layers, five different lifecycles.

**Say:** "Each layer changes at a different rate. System instructions almost never change. Task context changes every single call. Conflating them is the single most common root cause of 'the agent did something inconsistent' bug reports."

---

## Slide 6 — Architecture: instruction hierarchy (§3.4)

**On slide:** Who is the agent? What may it use? How does it reason about uncertainty? What must it never do?

**Say:** "User content — an account note, a retrieved page — can never answer these questions. It can only ever be evidence. That's not a policy we hope the model follows; today we make it structurally true in the code that assembles context."

---

## Slide 7 — Seven Steps mapping

**On slide:** Primary: Build Context. Supporting: Frame the Use Case, Evaluate & Govern.

**Say:** "Build Context comes before Design Agent Capabilities for a reason — you cannot design a good tool or Skill without already knowing what information environment it operates inside."

---

## Slide 8 — Gemini vs. deterministic code

**On slide:** The model reasons over context. Code decides what enters it.

**Say:** "By the end of today, look at `context_builder.py` — there is not one call to a model anywhere in it. Everything here is deterministic, testable Python. That's what 'engineering the context' actually means."

---

## Slide 9 — Security: prompt-injection-shaped failures (§3.6)

**On slide:** "A malicious note that attempts to override policy" — one of today's four required tests.

**Say:** "We're going to write a test with a note that says 'ignore all previous instructions.' We can't yet test whether a real model obeys it — no model call exists yet. What we *can* test, right now, deterministically, is whether that text ever has the structural opportunity to reach the same trust tier as system instructions. Today's guarantee is architectural, not behavioral — Class 3 is where we'll see how a real model actually responds."

---

## Slide 10 — Today's increment

**On slide:** `config/*.yaml`, `instructions.py`, `context_builder.py`.

**Say:** "Three YAML files carrying WidgetWare's actual business rules, one fixed instructions constant, and one assembly function. That's the whole context architecture."

---

## Slide 11 — Lab architecture: the four context tests

**On slide:** Qualified account, unqualified account, insufficient-evidence account, malicious note.

**Say:** "We'll build the malicious-note test live, and deliberately let it fail first, so you see what 'context wasn't properly isolated' actually looks like before we fix it."

---

## Slide 12 — Acceptance criteria

**On slide:** Injected instructions fail to override system constraints. Context is compact enough to inspect manually.

**Say:** "Print the assembled prompt today, at least once, and actually read it top to bottom. If you can't hold the whole thing in your head, it's already too big — and that problem only gets worse starting Book 2."
