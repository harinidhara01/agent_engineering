# Class 8 — Multi-Agent Workflow and Human Approval

**Manuscript source:** Book 1, Chapter 9 — Multi-Agent Workflows and Human Approval
**Seven-Step mapping:** Primary: Orchestrate Workflows / Supporting: Design Agent Capabilities, Evaluate & Govern
**Golden solution produced:** `class-08/golden-solution/`
**Starting checkpoint:** `class-07/golden-solution/`

## 0:00–0:30 — Homework review, common mistakes, golden solution reveal

- **Review homework:** ask participants to show a `ResearchBrief` with a real `conflicts[]` entry and explain what would have happened if their fix had silently picked a winner instead.
- **Common mistakes to flag:** freshness checks that flag stale evidence but don't change downstream behavior; research pipelines that quietly re-trust content after the injection-attempt test passes once.
- **Golden solution reveal:** walk `class-07/`'s `ResearchBrief`, then ask: research and qualification both exist now, as two separate capabilities — who coordinates them, and who decides when a human has to look?

## Slide outline (0:30–0:55)

1. Current WidgetWare state: qualification and research both work, independently, uncoordinated
2. Today's dependency: both prior chapters' typed contracts become handoff payloads between agents
3. Business objective: one coordinated workflow ending in a human approval gate, never an autonomous send
4. Core concept: why multiple agents (§9.1) — Research Agent, Evidence Reviewer, Drafting Agent, each with one responsibility
5. Terminology: workflow patterns (§9.2); typed handoffs (§9.4)
6. Architecture: state machine before agent prompt (§9.3) — the explicit states this workflow can be in
7. Seven Steps mapping: Orchestrate Workflows, the first chapter primarily about *coordination* rather than a single agent's capability
8. Gemini vs. deterministic code: each agent reasons within its role; code enforces which state transitions are legal
9. Security: human-in-the-loop approval (§9.6) as a workflow state and policy decision, not an instruction asking politely
10. Today's increment: Research → Qualify → Review → Draft → `AWAITING_APPROVAL`
11. Lab architecture: partial failure (§9.7) — a visible state and next action for every failure mode, no full restarts
12. Acceptance criteria: outreach is based only on Evidence-Reviewer-approved claims; no send tool exists anywhere in this codebase

## Kahoot (6–8 questions)

- Terminology: What does a "typed handoff" pass between agents that an open conversation history wouldn't (§9.4, and Book 2 Ch6's later A2A analogy)?
- Terminology: Name the five explicit states this workflow can occupy on its way to approval.
- Architecture: Why is the state machine designed before the agent prompts, per §9.3?
- Architecture: What's the Evidence Reviewer's one job, and why is it separate from the Drafting Agent?
- Failure analysis: The Drafting Agent fails mid-workflow — does the whole run restart? What does §9.7 say instead?
- Security/governance: What makes human approval "a workflow state and policy decision" rather than a courtesy prompt?
- WidgetWare scenario: A draft contains a claim the Evidence Reviewer never approved — what should block it?
- Connecting back: How does this chapter's approval package reuse the qualification contract from Class 4 and the research brief from Class 7?

## Build together (1:05–1:35)

Following the Hands-on Lab in Book 1 §9:

- agent modules for research, qualification, review, and drafting (research and qualification already exist — wire them in; review and drafting are new)
- workflow contracts connecting each stage's typed output to the next stage's typed input
- deterministic state transitions (the explicit state machine from §9.3)
- an approval record and a simple local approval interface
- checkpoint persistence
- scenario tests: success, insufficient evidence, source conflict, malformed output, rejected approval

End at `AWAITING_APPROVAL`. Confirm out loud, as a class, that no send tool exists in the codebase — this is the moment to make Book 1's standing external-action boundary (Class 1, §1.6) visible as an actual absence in the code, not a policy statement.

## Test and diagnose (1:35–1:50)

1. Run the full-success scenario test (happy path, ending at `AWAITING_APPROVAL`).
2. Run the approval-record contract test (this chapter's schema/contract equivalent).
3. Trigger a partial failure deliberately — kill the Drafting Agent mid-run — and confirm the workflow reports a visible state instead of losing the completed research and qualification work.
4. Inspect the workflow's persisted checkpoint and resume from it.
5. Diagnose using the Framework's seven categories — this class's failures are almost always **workflow state** issues (an illegal transition allowed, or a legal one blocked).
6. Apply the smallest fix — usually a missing guard in the state machine, not a change to any individual agent.
7. Re-run all five scenario tests.

## Homework

| Level | Task |
| ----- | ---- |
| **Required** | Full workflow runs research through `AWAITING_APPROVAL` for at least two accounts, resumable from a checkpoint after a simulated interruption |
| **Diagnostic** | The provided rejected-approval test case currently lets a rejected draft silently disappear instead of producing a visible `REJECTED` state — fix it |
| **Extension** | Add a sixth partial-failure scenario not covered in class (from §9.7's list) with its own test |

- **Starting checkpoint:** `class-07/golden-solution/`
- **Files participants may modify:** `src/widgetware_sdr/workflow/`, `src/widgetware_sdr/agents/review_agent.py`, `src/widgetware_sdr/agents/drafting_agent.py`, `tests/`
- **Expected behavior:** every one of the five scenarios ends in a visible, correct state; no partial failure loses prior successful work; no code path can send anything externally
- **Tests that must pass:** all five scenario tests (success, insufficient evidence, source conflict, malformed output, rejected approval)
- **Submission:** a resumed-from-checkpoint run's terminal output, plus a grep of the codebase confirming no send/CRM-write function exists
- **Constraints:** the workflow must terminate at `AWAITING_APPROVAL` or a named failure state — never at "sent"

## Golden solution: `class-08/`

Adds `workflow/`, the review and drafting agents, checkpoint persistence, and all five scenario tests on top of `class-07/`. README states the Chapter 9 checkpoint verbatim: "WidgetWare is now a complete bounded agent system" — and flags that Class 9 is where we prove it's actually good enough, not just complete.

## Bridge to Class 9

Class 9 asks whether this system is good enough to ship: a golden dataset, evaluation layers, release gates, deployment — and then wraps the whole workflow in a bounded, unattended ADK loop.
