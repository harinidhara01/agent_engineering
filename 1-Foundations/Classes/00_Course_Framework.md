# Agent Engineering with Gemini, ADK & Antigravity — Book 1 Ten-Class Program

This is the instructor-facing companion to the Gemini edition's **Book 1**. It turns Book 1 into an **ten-class, cumulative course** — two hours per class, one class per chapter, same rhythm every class, one running codebase (WidgetWare SDR Lab) from Class 1 through the close of Book 1.

Book 2 is a separate, equally-sized program — its own ten classes, one per Book 2 chapter — continuing the same WidgetWare system into enterprise-platform territory. It is not part of this document's numbering.

The manuscript teaches the reader. This program teaches a cohort, together, in a room, against a shared clock. The two are meant to be used side by side: each class's lecture segment draws directly from one named Book 1 chapter, and the class's lab is that chapter's own Hands-on Lab, run live instead of read.

## Why the cadence is fixed and the topic isn't

Every class uses the same nine-segment structure, in the same order, for the same durations. Only the content changes. This is deliberate: a participant should never spend classroom time relearning how class works — attention should go entirely to the material. By Class 2, the rhythm is invisible; by Class 10, it is the thing that made eleven different chapters feel like one course instead of eleven lectures stitched together.

## Standard Two-Hour Class Cadence

|      Time | Segment                                       | Purpose                                                                        |
| --------: | ---------------------------------------------- | ------------------------------------------------------------------------------- |
| 0:00–0:10 | **Review the previous homework**              | Ask participants to explain what they built, what worked, and where they struggled |
| 0:10–0:20 | **Discuss common mistakes**                   | Review recurring design, coding, configuration, and conceptual errors           |
| 0:20–0:30 | **Share the previous golden solution**        | Demonstrate the reference implementation and explain the important engineering decisions |
| 0:30–0:55 | **Explain today's concepts and architecture** | Teach the concepts, show the architecture, map them to the Seven Steps, and explain the WidgetWare increment |
| 0:55–1:05 | **Check understanding with Kahoot**           | Run 6–8 questions covering concepts and architecture                           |
| 1:05–1:35 | **Build the capability together**             | Instructor-led implementation with participants following in their own repositories |
| 1:35–1:50 | **Run tests and diagnose failures**           | Execute tests, inspect outputs, trace failures, and demonstrate debugging techniques |
| 1:50–1:57 | **Compare with the golden solution**          | Show differences between the class implementation and the reference version    |
| 1:57–2:00 | **Assign the exercise as homework**           | Explain the completion task, expected artifacts, tests, and acceptance criteria |

## The Learning Loop

Every class follows the same progression:

> **Review → Diagnose → Reveal → Explain → Check → Build → Test → Compare → Complete**

This works for Agent Engineering specifically because participants repeatedly experience three complementary perspectives on the same problem:

1. **Their own attempt** (last night's homework)
2. **The instructor-led implementation** (built live, in class)
3. **The tested golden solution** (the reference checkpoint)

They do not copy code from one source. They compare three independently-arrived-at answers to the same problem and learn to explain why the reference solution is shaped the way it is — which is the same "probabilistic reasoning inside deterministic boundaries" habit the manuscript itself teaches (Book 1, Chapter 1.4), now applied to the participants' own work instead of WidgetWare's.

## Class 1 Exception

Class 1 has no previous homework and no previous golden solution to reveal. Its first 30 minutes replace segments 1–3 with:

|      Time | Class 1 opening                                                                |
| --------: | -------------------------------------------------------------------------------- |
| 0:00–0:10 | Introductions, course goals, participant expectations                          |
| 0:10–0:20 | Ten-class Book 1 course architecture and final outcome (a loop-ready, evaluated agent platform) |
| 0:20–0:30 | WidgetWare SDR case study, repository structure, and the cumulative learning model |

From **Class 2 onward**, use the standard nine-segment cadence without modification.

## What the Golden Solution Should Contain

Every class produces a versioned, runnable reference checkpoint:

```text
golden-solutions/
├── class-01/
├── class-02/
├── class-02/
├── class-03/
├── class-04/
├── class-05/
├── class-06/
├── class-07/
├── class-08/
├── class-09/
└── class-10/
```

Each checkpoint includes:

- complete source code through that class;
- configuration files;
- sample inputs;
- expected outputs;
- automated tests;
- a short README;
- known failure cases;
- a completion checklist; and
- instructions for starting the next class.

Every checkpoint is **cumulative and independently runnable**. A participant who misses Class 3 starts Class 4 from the Class 3 golden solution, not from their own unfinished work — the golden solution is the course's actual continuity mechanism, not a bonus artifact.

## Homework Pattern

Every homework assignment has three levels:

| Level          | Expectation                                                              |
| -------------- | ------------------------------------------------------------------------- |
| **Required**   | Complete the capability built during class and pass the provided tests  |
| **Diagnostic** | Fix one intentionally introduced failure or edge case                   |
| **Extension**  | Add a small enhancement using the concepts taught that day               |

The required portion should normally take 30–45 minutes. The extension is optional for faster or more experienced participants.

Every assignment specifies, without exception:

- starting checkpoint;
- required changes;
- files participants may modify;
- expected behavior;
- tests that must pass;
- output or screenshot to submit; and
- constraints and prohibited shortcuts.

## Recommended Slide Cadence

The 0:30–0:55 conceptual segment runs approximately 10–12 slides, roughly two minutes of speaking notes each:

1. Current WidgetWare state
2. Previous capability and today's dependency
3. Today's business objective
4. Core concept
5. Supporting terminology
6. Architecture diagram
7. Seven Steps mapping
8. Gemini versus deterministic-code responsibilities
9. Security and trust boundaries
10. Today's WidgetWare increment
11. Lab architecture
12. Acceptance criteria

## Kahoot Cadence

Each class runs 6–8 questions, embedded in the flow rather than as a standalone quiz, covering:

- two terminology questions;
- two architecture or design-choice questions;
- one failure-analysis question;
- one security or governance question;
- one WidgetWare scenario question; and
- one question connecting today's work to a previous class.

The purpose is to verify readiness to build, not to grade memorization.

## Testing Cadence

The 1:35–1:50 segment follows the same seven-step sequence every class:

1. Run the happy-path test.
2. Run the contract or schema test.
3. Trigger one intentional failure.
4. Inspect the error, log, trace, or agent event.
5. Diagnose whether the failure comes from context, model behavior, tool implementation, contract validation, workflow state, permissions, or evaluation criteria.
6. Apply the smallest correct fix.
7. Re-run the tests.

This reinforces that testing and diagnosis are part of Agent Engineering, not activities postponed until the final class — the same discipline the manuscript itself insists on from Book 1, Chapter 4.5 onward.

## Ten-Class Application

| Class | Manuscript source | Main capability | Homework outcome |
| ----: | ------------------ | ---------------------------------------------------------- | ------------------------------------------------------ |
|     1 | Book 1, Ch. 1–2 | Agent Engineering foundations, the WidgetWare specification, and the Antigravity repository harness | Complete the scoped use case, acceptance criteria, and a passing `./scripts/check.sh` |
|     2 | Book 1, Ch. 3 | Gemini context and instruction architecture | Refine WidgetWare context and test prompt behavior |
|     3 | Book 1, Ch. 4 | First ADK agent (embedded procedure) | Complete the account-qualification agent |
|     4 | Book 1, Ch. 5 | Skills and reusable agent capabilities | Extract the qualification procedure into a Skill |
|     5 | Book 1, Ch. 6 | Structured outputs and agent contracts | Add a validated `QualificationResult` contract |
|     6 | Book 1, Ch. 7 | Tool engineering | Attach the agent's first read-only tools |
|     7 | Book 1, Ch. 8 | MCP and evidence-backed research | Produce a cited account-research brief |
|     8 | Book 1, Ch. 9 | Multi-agent workflow and human approval | Complete the approved outreach workflow |
|     9 | Book 1, Ch. 10 | Evaluate, deploy, and demonstrate | Pass the golden-dataset release gate |
|    10 | Book 1, Ch. 11 | Loop engineering with ADK | Run the unattended batch loop to completion |

Every class tracks exactly one Book 1 chapter, at a one-to-one pace, with one deliberate exception: Class 1 merges Chapters 1 and 2 — the charter and the repository harness — because a charter nobody can run is a weaker first checkpoint than one paired with a workspace that proves it's real (see `class-01/golden-solution/docs/architecture-decisions/0003-repository-harness.md`). No other chapter is split across classes and no other two chapters share a class. Class 10 closes Book 1.

Per-class lesson plans: `class-0N/lesson-plan.md`.
