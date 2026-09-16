# Class 10 Kahoot — 8 Questions

Run during 0:45–0:55. Correct answer marked with **✓**.

---

**1. (Terminology)** What are the five outcomes of the loop's per-account decision (§11.8)?
- **✓** A) CONTINUE, RETRY, STOP, DEFER, ESCALATE
- B) PASS, FAIL, SKIP, RETRY, ABORT
- C) QUALIFIED, NOT_QUALIFIED, NEEDS_RESEARCH, BLOCKED, APPROVED
- D) SUCCESS, ERROR, TIMEOUT, PENDING, DONE

**2. (Terminology)** What's the difference between the inner agent loop ADK already runs and the outer loop this chapter adds (§11.2–11.3)?
- **✓** A) The inner loop is one agent's own observe-reason-act cycle within a single call; the outer loop decides what to work on next across many separate invocations
- B) There is no difference — both terms describe the same mechanism
- C) The inner loop only exists in Book 2
- D) The outer loop replaces the inner loop entirely

**3. (Architecture)** Why is `max_iterations` alone not an engineered loop (§11.4)?
- **✓** A) It bounds how many times the loop can run but says nothing about work selection, durable state, verification, or budgets
- B) ADK does not actually support `max_iterations` as a real parameter
- C) It is sufficient on its own; the rest of the chapter is optional polish
- D) `max_iterations` only applies to inner reasoning loops, never outer ones

**4. (Architecture)** Why does the state machine need `RETRY_PENDING` and `NEEDS_HUMAN_REVIEW` added, and why is `BLOCKED` no longer terminal once they exist?
- **✓** A) A batch loop needs a way to distinguish "worth retrying automatically" from "needs a person" — collapsing both into a terminal `BLOCKED` would make that distinction impossible to act on
- B) They're purely cosmetic renames of existing states
- C) `BLOCKED` was always non-terminal, even before Class 10
- D) These states only matter for live-model integration tests

**5. (Failure analysis)** A restarted batch run re-researches an account it already finished. What's missing?
- **✓** A) Durable session state — likely an `InMemorySessionService` used where a persistent one was needed
- B) A bigger context window
- C) A better system prompt
- D) Nothing is missing; re-researching a finished account is expected behavior

**6. (Security/governance)** Does an account processed inside an unattended batch loop get less approval scrutiny than one processed on request?
- **✓** A) No — §11.10 says the authority table from Class 8 applies identically, whether or not a person is watching
- B) Yes, batch-processed accounts are auto-approved for efficiency
- C) Only accounts above a certain fit score skip approval
- D) Approval only matters for the first account in a batch

**7. (WidgetWare scenario)** The loop hits its maximum-attempts limit for one account. Which decision?
- **✓** A) ESCALATE — attempts are exhausted, so it routes to `NEEDS_HUMAN_REVIEW` rather than retrying or discarding it
- B) RETRY — always retry regardless of the limit
- C) STOP — the entire batch run halts because of one account
- D) CONTINUE — silently skip and move to the next account with no record

**8. (Connecting back)** How does the loop's verification-before-advancing step (§11.7) reuse Class 5's contracts and Class 8's state machine?
- **✓** A) It trusts only the state the Class 8 state machine actually reached and only contract objects that passed Class 5's validation — never an agent's own unverified claim about what happened
- B) It doesn't — verification is a new mechanism unrelated to earlier classes
- C) It replaces the state machine with a simpler boolean flag
- D) It only applies to the final account in the queue

---

## Facilitator notes

- Question 6 is the class's most important idea — the same one Kahoot question 6 tested in Class 6 for a single tool's permissions, now re-tested at the scale of an entire unattended run. Worth naming that repetition out loud.
- Question 3 pairs well with a live demonstration: construct a `LoopAgent` with only `max_iterations` set and ask the room what's missing before revealing the full budget/decision/queue machinery.
