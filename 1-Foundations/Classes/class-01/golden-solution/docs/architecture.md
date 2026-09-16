# Architecture

This document describes the **destination** architecture for WidgetWare SDR Lab and where this checkpoint sits on the way there. It is not a claim about what exists in code today — `SPEC.md` and the completion checklist in `README.md` are the source of truth for that.

## The destination

```text
Target account
   │
   ▼
Retrieve internal account context  ─┐
Research permitted public evidence  │  (Class 6–7, Book 1 Ch. 7–8)
   ▼                                │
Evaluate against configured ICP    ─┘  (Class 2–4, Book 1 Ch. 3–5)
   ▼
Structured qualification result        (Class 4–5, Book 1 Ch. 5–6)
   ▼
Evidence-backed outreach draft         (Class 8, Book 1 Ch. 9)
   ▼
Human approval gate                    (Class 8, Book 1 Ch. 9)
   ▼
(no further capability exists — Book 1 never adds a send tool)
```

## What this checkpoint (Class 1) actually contains

- A business brief and specification describing the destination above.
- A repository harness capable of proving, mechanically, that the repository is in a known-good state: `pyproject.toml`, an installable `widgetware_sdr` package, a deterministic health check, and one command (`scripts/check.sh`) that verifies formatting, linting, typing, and tests.
- Three representative scenario accounts and their expected qualification direction, as fixtures — not yet checked by any code, since there is no qualification logic yet to check them against.

Nothing in the diagram above from "Evaluate against configured ICP" onward exists in this checkpoint's code. `config/` is present and empty. `src/widgetware_sdr/` contains only the health check.

## Why the harness comes this early

A development harness — repository structure, dependency management, a one-command quality gate, documented conventions — is not scaffolding to discard once "real" work starts. It is part of the system, in the same sense that a building's foundation is part of the building. Every capability added in a later class inherits whatever discipline (or sloppiness) this checkpoint establishes. See `docs/architecture-decisions/0003-repository-harness.md`.

## Layering principle

Two kinds of code will eventually exist in this repository, and this checkpoint's own structure already reflects the separation, even though only one side has content yet:

- **Deterministic code** — validation, configuration loading, state transitions, the health check. Fully specified, fully tested, no model involved. This is everything currently in `src/`.
- **Model-mediated reasoning** — interpretation, synthesis, drafting. Starts in Class 3 (Book 1, Chapter 4) with the first ADK agent. None of it exists yet.

The repository structure — `src/`, `config/`, `tests/{unit,contracts,scenarios}` — is designed so that when model-mediated reasoning is added, it is additive to this structure, not a rewrite of it.
