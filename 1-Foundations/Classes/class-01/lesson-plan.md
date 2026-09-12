# Class 1 — Agent Engineering Foundations and the Antigravity Repository Harness

**Manuscript source:** Book 1, Chapters 1 and 2 — From Language Models to Agent Engineering; Building with Antigravity
**Seven-Step mapping:** Primary: Frame the Use Case, Build the Harness / Supporting: Design Agent Capabilities, Evaluate & Govern
**Golden solution produced:** `golden-solutions/class-01/`

Class 1 now merges what used to be two separate classes. The reasoning is in `golden-solution/docs/architecture-decisions/0003-repository-harness.md`: a charter nobody can run is a weaker first checkpoint than a charter paired with the harness that makes it verifiable. This is a denser class than the ones that follow it — plan the pacing below deliberately, and don't be surprised if the "build together" segment runs a few minutes long the first time you teach it.

## Cadence for this class (Class 1 exception — see Framework §"Class 1 Exception")

|      Time | Segment |
| --------: | ------- |
| 0:00–0:10 | Introductions, course goals, participant expectations |
| 0:10–0:20 | Ten-class course architecture and the final outcome (the unattended batch loop) |
| 0:20–0:30 | WidgetWare SDR case study, repository structure, and the cumulative learning model |
| 0:30–0:55 | Explain today's concepts: Frame the Use Case *and* Build the Harness |
| 0:55–1:05 | Kahoot check |
| 1:05–1:35 | Build together: charter, then harness |
| 1:35–1:50 | Test and diagnose |
| 1:50–1:57 | (No prior golden solution — instead, preview what "golden solution" means starting Class 2) |
| 1:57–2:00 | Assign homework |

From Class 2 onward, the standard nine-segment cadence in `../00_Course_Framework.md` applies unmodified.

## Slide outline (0:30–0:55)

Twelve slides split roughly in half between the two chapters. Move briskly through the first six — participants will spend more time with these ideas in the build segment than in the lecture.

1. What this course builds, end to end (the ten-class arc, not just today)
2. A model is a capability, not a system (Book 1, §1.1); the autonomy spectrum (§1.3) — WidgetWare stops at level 4, Prepare
3. Probabilistic reasoning inside deterministic boundaries (§1.4) — the idea the whole course keeps returning to
4. Introducing WidgetWare (§1.5) and the initial system boundary (§1.6) — what this system may never do without a human
5. Acceptance criteria written before implementation (§1.7) — testable signals, not "looks good"
6. Today's WidgetWare increment, part one: the charter — five files, zero code, still true even though code arrives later today
7. **Bridge:** a charter nobody can run is a weaker checkpoint — today doesn't stop there
8. The harness is part of the system (§2.1) — not scaffolding you discard later
9. Antigravity as engineering partner; `README.md` vs. `SPEC.md` (§2.2, §2.4); repository structure (§2.3)
10. Trust and permissions for a *development* agent (§2.7) — least privilege applies before anything sensitive exists
11. Today's WidgetWare increment, part two: the harness — installable package, health check, one-command gate
12. Acceptance criteria, reprised: every Section A criterion in `docs/acceptance-criteria.md` is checked by `./scripts/check.sh` by the end of today

## Kahoot (8 questions)

- Terminology: What distinguishes an agent from a workflow?
- Terminology: What's the difference between `README.md` and `SPEC.md` in this repository convention?
- Architecture: Why does Book 1 forbid an external send action from day one?
- Architecture: Why does the repository harness belong in Class 1 now, instead of a separate class?
- Failure analysis: A system drafts a confident recommendation with no supporting evidence — what's missing?
- Security/governance: What must be true before WidgetWare is allowed to modify a CRM record? Name one thing "least privilege" means for a *development* agent specifically.
- WidgetWare scenario: Given an account outside the ICP, what should the system do?
- Connecting forward: What does this class deliberately leave unbuilt for later classes, even though real code now exists?

## Build together (1:05–1:35)

Two parts, back to back. Keep both tightly scoped — this segment covers what used to be two classes' worth of building.

**Part one — the charter (≈12 minutes):**
- Have participants draft `docs/acceptance-criteria.md` themselves, in pairs, before revealing the reference version.
- Fill in `README.md`, `SPEC.md`, `docs/widgetware-business-brief.md`, and the three scenario descriptions under `tests/scenarios/` at a brisk pace — the point is having an opinion about "success," not perfecting the prose live.

**Part two — the harness (≈18 minutes):**
- Give Antigravity the deliberately vague task first — "set up the project" — and look at what it produces.
- Then give it the properly scoped task (see `BUILD.md` step 7 for the exact prompt): `pyproject.toml`, `src/widgetware_sdr` with a health check, matching tests, `.env.example`, `.gitignore`, `scripts/verify_environment.py`, and `scripts/check.sh` running environment verification, formatting, linting, typing, and tests in order.
- The comparison between the two attempts — not either output alone — is Book 1 §2.6's actual lesson.
- Add `.agents/rules/`, `.agents/workflows/`, `CONTRIBUTING.md`, and `SECURITY.md` from the reference if time is short; these are good homework-Diagnostic material if the room is behind schedule.

## Test and diagnose (1:35–1:50)

1. Run `./scripts/check.sh` for the first time — this is also the first time in the course something actually runs.
2. Walk the five stages in order: environment verification, format check, lint, type check, tests. Name what each one catches that the others don't.
3. Trigger a failure on purpose: comment out a required file, or reintroduce a formatting error, and watch which stage catches it.
4. Trigger a second, different failure: paste a plausible-looking (but fake) API key string into a tracked file and run `pytest tests/unit/test_repository_contract.py -k credential` to show the credential-shape check catching it.
5. Diagnose against the Framework's seven categories — today's failures are almost always "context" (a rule was never written down anywhere Antigravity would read it) or "permissions" (a generated script requested more than the task needed).
6. Apply the smallest fix. Re-run `./scripts/check.sh` clean.

## Homework

| Level | Task |
| ----- | ---- |
| **Required** | Finish the charter and harness together; get `./scripts/check.sh` passing cleanly from a fresh clone; commit the repository |
| **Diagnostic** | Take one acceptance criterion and rewrite it until a stranger could evaluate a system against it without asking a clarifying question |
| **Extension** | Add `.agents/`, `CONTRIBUTING.md`, and `SECURITY.md` if not finished in class, or draft one additional disqualifying scenario beyond the three covered |

- **Starting checkpoint:** none — this is the first commit
- **Files participants may modify:** everything created in class
- **Expected behavior:** `./scripts/check.sh` passes cleanly, covering environment verification, formatting, linting, typing, and tests
- **Tests that must pass:** all of `tests/unit/`
- **Submission:** the full repository, committed, plus the terminal output of a clean `./scripts/check.sh` run
- **Constraints:** no Gemini call, no ADK import, no network call, no send-capable code — this class is charter and harness only

## Golden solution: `class-01/`

Contains the full merged checkpoint: charter documents, architecture and ADRs, agent rules and workflows, the installable package, the health check, and `./scripts/check.sh`, verified to pass in a clean environment. See `golden-solution/README.md` for the exact Quick Start sequence and `golden-solution/KNOWN_FAILURE_CASES.md` for what this checkpoint honestly does not yet prove.

## Bridge to Class 2

Class 2 (Book 1, Chapter 3) gives Gemini its first real context architecture — separating stable policy, task data, and retrieved evidence — before Class 3 gives the system its first actual agent. Nothing about today's harness changes; Class 2 only adds to `config/` and `src/widgetware_sdr/`.
