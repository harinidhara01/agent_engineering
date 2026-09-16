# Class 1 Kahoot — 8 Questions

Run during 0:55–1:05. Import into Kahoot as single-select multiple choice unless noted. Correct answer marked with **✓**.

---

**1. (Terminology)** What distinguishes an agent from a workflow?
- A) An agent is faster than a workflow
- **✓** B) An agent selects or adapts actions toward a goal; a workflow follows a predefined sequence of steps
- C) A workflow always uses a language model; an agent never does
- D) There is no meaningful difference

**2. (Terminology)** What's the difference between `README.md` and `SPEC.md` in this repository convention?
- **✓** A) `README.md` serves people; `SPEC.md` defines required and prohibited behavior for the implementation
- B) They serve the same purpose and either name works
- C) `SPEC.md` is only used by Antigravity, never read by humans
- D) `README.md` is generated automatically and should never be edited

**3. (Architecture)** Why does Book 1 forbid an external send action from day one?
- **✓** A) Because autonomy should be designed and earned, not assumed, and WidgetWare hasn't yet proven it deserves that level of trust
- B) Because Gemini cannot draft outreach messages
- C) Because ADK does not support tools with side effects
- D) Sending is technically impossible in this architecture

**4. (Architecture)** Why does the repository harness belong in Class 1 now, instead of a separate class?
- **✓** A) A charter that cannot be mechanically verified is a weaker first checkpoint than one paired with a workspace that can prove it's real
- B) Because Antigravity requires a harness to generate any charter document
- C) It doesn't — the harness is still a separate class
- D) Because the manuscript itself merges Chapters 1 and 2

**5. (Failure analysis)** A system drafts a confident recommendation with no supporting evidence. What's missing?
- A) A faster model
- **✓** B) The evidence-or-labeled-inference requirement from the acceptance criteria
- C) More prompt engineering
- D) A bigger context window

**6. (Security/governance)** Name one thing "least privilege" means for a *development* agent specifically, before it modifies a CRM record.
- **✓** A) Restrict its access to production credentials, even though it can execute commands and modify files — and no CRM write happens at all without a prior human approval
- B) Give it full production access so it can fix anything
- C) Development agents don't need permission restrictions, only production agents do
- D) Least privilege only applies to WidgetWare's own tools, not to Antigravity itself

**7. (WidgetWare scenario)** Given an account outside the ICP (wrong industry, too small), what should the system do?
- A) Qualify it anyway and let a human catch the mistake later
- **✓** B) Return `NOT_QUALIFIED` with the specific exclusion criteria named
- C) Silently skip the account with no output
- D) Ask the model to use its best judgment regardless of the ICP

**8. (Connecting forward)** What does this class deliberately leave unbuilt for later classes, even though real code now exists?
- **✓** A) Any Gemini call, any ADK agent, any qualification logic, any tool — this class is charter and harness only
- B) The business brief
- C) The health check
- D) Nothing — the harness makes this checkpoint feature-complete

---

## Facilitator notes

- Questions 1–2 confirm vocabulary before it gets used casually for the rest of the course.
- Question 4 replaces the old "why does Book 1 forbid code in Class 1" framing — the answer has changed, and it's worth naming that explicitly if any returning participants ask.
- Question 8 is the class's most important check. The most common early confusion under the *new* structure is the opposite of the old one: participants who see real, passing tests for the first time sometimes assume more exists than actually does. Confirm out loud: no model call, no agent, no qualification logic — just a harness proven to work.
