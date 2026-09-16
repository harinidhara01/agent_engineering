# WidgetWare SDR Lab

A bounded agent system that researches, qualifies, and drafts outreach to prospective manufacturing and industrial-automation accounts on WidgetWare's behalf — and stops for human approval before anything leaves the building.

This repository is built incrementally across the ten-class Agent Engineering with Gemini, ADK & Antigravity course (Book 1). This checkpoint (Class 1 / `golden-solutions/class-01/`) merges Book 1's Chapters 1 and 2: the project charter **and** the repository harness. It is the **first runnable, reproducible, known-good baseline** in the course — not a documents-only artifact. It does not yet contain a Gemini model call or an ADK agent; that begins in Class 3 (Book 1, Chapter 4).

## What this system does (once complete)

Given a target company, WidgetWare SDR Lab will:

1. Retrieve any account information WidgetWare already has.
2. Research permitted public evidence about the company.
3. Evaluate fit against WidgetWare's configured ideal-customer profile.
4. Produce a structured qualification result.
5. Draft an evidence-backed outreach message.
6. Stop and request human approval before anything is sent.

See `SPEC.md` for the full behavioral contract, `docs/architecture.md` for how the destination system is put together, and `docs/acceptance-criteria.md` for how "done" is measured — both for this checkpoint and for the finished product.

## Quick start

No cloud credentials are needed for anything in this checkpoint.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
./scripts/check.sh      # verifies the environment, then formats, lints, types, and tests
```

`.env.example` documents the variable names a later class will read — nothing in this checkpoint reads them yet, so there is no need to create a local `.env` until a class actually asks for one. `verify_environment.py` confirms `.env` isn't part of the checkpoint at all yet, which is the expected state here, not a warning sign.

Expected: `verify_environment.py`, `ruff format --check`, `ruff check`, `mypy`, and `pytest` all pass — no network access, no Google Cloud credentials, no Gemini or ADK runtime involved anywhere in this sequence.

## Repository structure

```text
widgetware-sdr/
├── README.md / SPEC.md / CONTRIBUTING.md / SECURITY.md / pyproject.toml / .env.example
├── .agents/
│   ├── rules/            # engineering.md, security.md — always-on agent rules
│   └── workflows/        # baseline-check.md — the reusable verify-from-clean procedure
├── docs/
│   ├── widgetware-business-brief.md
│   ├── acceptance-criteria.md
│   ├── architecture.md
│   └── architecture-decisions/   # ADR 0001–0003
├── config/                # empty until Class 2 (Book 1, Chapter 3)
├── src/
│   └── widgetware_sdr/    # __init__.py, health.py — the only code that exists yet
├── scripts/
│   ├── check.sh
│   └── verify_environment.py
├── tests/
│   ├── unit/              # test_health.py, test_repository_contract.py
│   ├── contracts/         # empty until Class 5
│   ├── scenarios/         # three scenario descriptions, in prose
│   └── fixtures/
│       ├── accounts/      # the same three scenarios, structured
│       └── expected/      # their expected qualification direction
└── artifacts/              # generated reports land here, gitignored contents
```

## Sample inputs and expected outputs

`tests/fixtures/accounts/` holds the three scenario accounts as structured YAML. `tests/fixtures/expected/` holds the qualification direction and rationale each one should produce, once a qualification agent exists to check them against. `tests/scenarios/*.md` explains each scenario in prose and links to its structured pair. `tests/unit/test_repository_contract.py` already verifies the *structure* of these fixture pairs (matching IDs, allowed direction values) — it cannot yet verify the qualification *decisions* themselves, since no code makes that decision yet.

## Known failure cases

See [`KNOWN_FAILURE_CASES.md`](KNOWN_FAILURE_CASES.md).

## Completion checklist

Before treating this checkpoint as done:

- [ ] `./scripts/check.sh` passes cleanly from a fresh clone.
- [ ] `pip install -e ".[dev]"` succeeds with no manual workaround.
- [ ] `docs/widgetware-business-brief.md` states the product, ICP, and exclusions in a form someone unfamiliar with WidgetWare could repeat back correctly.
- [ ] `SPEC.md` states required behavior, prohibited behavior, and completion criteria as falsifiable statements, not marketing language.
- [ ] Every criterion in `docs/acceptance-criteria.md` Section A names a specific, checkable signal, and is actually checked by `./scripts/check.sh`.
- [ ] All three `tests/scenarios/*.md` files have a matching pair in `tests/fixtures/accounts/` and `tests/fixtures/expected/`.
- [ ] `docs/architecture.md` and the three architecture decision records are present and consistent with `SPEC.md`.
- [ ] `.agents/rules/` and `.agents/workflows/` exist and describe real, followable practices.
- [ ] No credential, API key, or real project identifier is committed anywhere.
- [ ] No Gemini call, no ADK agent, and no send-capable code exists anywhere in this checkpoint.

## Starting Class 2

1. Start from this checkpoint as-is. Class 2 (Book 1, Chapter 3) does not change anything listed above — it only adds to `config/` and `src/widgetware_sdr/`.
2. Confirm `./scripts/check.sh` passes here first. Class 2 adds a new dependency (`PyYAML`) and new tests — starting from a broken Class 1 checkpoint makes it much harder to tell which failures are new.
3. See `../../class-02/golden-solution/README.md` for what Class 2 actually adds.

## Status

- [x] Class 1 — Foundations and repository harness (Book 1, Chapters 1–2)
- [ ] Class 2 — Gemini context and instruction architecture
- [ ] Classes 3–10 — see `../../00_Course_Framework.md`
