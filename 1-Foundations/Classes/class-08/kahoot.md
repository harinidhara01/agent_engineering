# Class 8 Kahoot — 8 Questions

Run during 0:55–1:05. Correct answer marked with **✓**.

---

**1. (Terminology)** What does a "typed handoff" pass between agents that an open conversation history wouldn't (§9.4)?
- **✓** A) A compact, well-defined contract — exactly the fields the next stage needs, nothing more
- B) The full transcript of every previous agent's reasoning
- C) A single free-text summary string
- D) Nothing — handoffs and conversation history are the same thing in ADK

**2. (Terminology)** Name the states this workflow can occupy on its way to approval.
- **✓** A) RECEIVED, RESEARCHING, RESEARCH_COMPLETE, QUALIFYING, REVIEW_REQUIRED, DRAFT_READY, AWAITING_APPROVAL
- B) START, MIDDLE, END
- C) PENDING, PROCESSING, DONE
- D) QUALIFY, REVIEW, SEND

**3. (Architecture)** Why is the state machine designed before the agent prompts, per §9.3?
- **✓** A) So valid transitions are enforced by code, not left to whatever a model happens to recommend
- B) Because ADK requires state machines to be defined first, as a technical constraint
- C) It isn't — prompts should always come first
- D) State machines are optional in Book 1 and only appear in Book 2

**4. (Architecture)** What's the Evidence Reviewer's one job, and why is it separate from the Drafting Agent?
- **✓** A) Verify claims are cited and current before anything gets drafted — separating "is this true and supported" from "how do we say it"
- B) To write the actual outreach message
- C) To calculate the fit score
- D) To decide the final approval — reviewers and approvers are the same role here

**5. (Failure analysis)** The Drafting Agent fails mid-workflow. Does the whole run restart?
- **✓** A) No — §9.7 says a visible state and next action should result, without losing the completed research and qualification work
- B) Yes, always restart from RECEIVED
- C) The workflow silently retries forever until it succeeds
- D) The account is permanently discarded

**6. (Security/governance)** What makes human approval "a workflow state and policy decision" rather than a courtesy prompt?
- **✓** A) The system is structurally unable to execute the external action without reaching an approved state — there's no send capability to bypass in the first place
- B) The model is simply instructed to always ask first, and that instruction is trusted
- C) Approval is optional and can be skipped for high-confidence accounts
- D) It isn't different from a courtesy prompt — same mechanism, different wording

**7. (WidgetWare scenario)** A draft contains a claim the Evidence Reviewer never approved. What should block it?
- **✓** A) Structurally, nothing — because the Drafting Agent should never have received an unapproved claim as input in the first place
- B) A human catching it during the approval step, as the only safeguard
- C) Nothing blocks it; drafts are allowed to include any claim
- D) The state machine, retroactively, after the draft is created

**8. (Connecting back)** How does this chapter's approval package reuse the qualification contract from Class 4 and the research brief from Class 7?
- **✓** A) The `ApprovalPackage` includes the qualification summary and supporting evidence drawn directly from those earlier typed contracts, not restated by hand
- B) It doesn't — the approval package is built entirely from scratch
- C) It replaces both contracts entirely
- D) Only the research brief is reused; qualification results are discarded before approval

---

## Facilitator notes

- Question 6 is the conceptual center of the whole class — spend the extra thirty seconds if the room needs it.
- Question 7 is worth pairing with a live demonstration: try to construct an `OutreachDraft` using a claim not in an `EvidenceReview`'s approved list, and show that nothing in the type system stops you directly — the guarantee comes from *what the drafting agent is given as input*, not from the contract alone. This nuance is worth surfacing explicitly.
