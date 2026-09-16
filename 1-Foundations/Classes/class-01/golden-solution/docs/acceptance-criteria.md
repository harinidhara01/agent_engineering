# Acceptance Criteria

This document has two sections, and they answer different questions. Keeping them separate matters: it is easy to accidentally judge this checkpoint against criteria that describe the *finished product*, months from now, instead of what this specific checkpoint can actually prove today.

## A. Class 1 checkpoint acceptance criteria

Executable or directly inspectable **right now**, against this repository as it exists at this checkpoint.

1. **Clean installation succeeds.** `python3 -m venv .venv && source .venv/bin/activate && pip install -e ".[dev]"` completes with no manual workaround, on a fresh clone.
2. **Environment verification succeeds.** `python3 scripts/verify_environment.py` exits `0` with no network access and no credentials present.
3. **The package imports.** `python3 -c "import widgetware_sdr"` succeeds, and `widgetware_sdr.__version__` matches `pyproject.toml`'s `project.version`.
4. **The health check succeeds deterministically.** `health_check()` returns the same structure on every call, with no network call, no model call, and no credential dependency.
5. **Formatting, linting, typing, and tests all pass.** `./scripts/check.sh` runs `verify_environment.py`, `ruff format --check`, `ruff check`, `mypy`, and `pytest` in that order, and all five stages pass.
6. **Required business, architecture, engineering, and security documents exist and are internally consistent.** `README.md`, `SPEC.md`, `docs/widgetware-business-brief.md`, `docs/architecture.md`, the three architecture decision records, `.agents/rules/*.md`, `.agents/workflows/*.md`, `CONTRIBUTING.md`, and `SECURITY.md` are all present, and none contradicts another on a fact that matters (ICP thresholds, the no-send boundary, the autonomy level).
7. **No credentials are committed.** No real API key, token, or project identifier appears anywhere in the tracked repository; `.env.example` documents variable names only, with placeholder values.
8. **No model, network, CRM, or send capability exists.** No source file imports a Gemini or ADK library; no function resembles a send-capable tool; no code makes an outbound network call.
9. **Scenario and fixture pairs are structurally valid.** All three scenarios in `tests/scenarios/` have a matching account fixture and expected-result fixture, each expected fixture's `account_id` matches its account fixture's `account_id`, and the three expected qualification directions together cover `QUALIFIED`, `NOT_QUALIFIED`, and `NEEDS_RESEARCH`.
10. **The checkpoint can serve as the baseline for the next class.** A learner who runs nothing but the "Quick start" sequence in `README.md` ends up with a passing `./scripts/check.sh`, ready to begin Class 2 (Book 1, Chapter 3) without any undocumented setup step.

Every criterion above is checked automatically by `tests/unit/test_repository_contract.py` and `tests/unit/test_health.py`, except criterion 6's editorial consistency, which the qualitative review in `GRADING.md` covers.

## B. Future WidgetWare product acceptance criteria

**Not implemented yet.** These describe the completed system this course builds toward across the rest of Book 1 — they are commitments the specification makes about the destination, not capabilities this checkpoint has. Do not test this checkpoint against them; there is no qualification agent, no contract, and no evidence pipeline yet for them to apply to.

1. **Schema conformance.** Every qualification result the finished system produces validates against a published schema (introduced Class 5 / Book 1, Chapter 6). A result that does not validate is never surfaced as if it were a valid answer.
2. **Evidence or labeled inference.** Every material factual claim in a qualification result or outreach draft either references a specific piece of supplied or retrieved evidence, or is explicitly labeled as an inference.
3. **No drafting on insufficient evidence.** When evidence does not support a qualification decision either way, the system produces `NEEDS_RESEARCH` and does not draft outreach.
4. **No autonomous send.** No test run, demonstration, or production path ever transmits an outbound message without a preceding, explicit human approval — verified by the structural absence of any send-capable tool (see `docs/architecture-decisions/0002-no-outbound-send.md`), not merely by observing that no test happened to trigger one.
5. **Explainability.** For any qualification result, a person can ask "why this decision?" and receive an answer naming the specific matched or failed ICP criteria and the evidence behind them.
6. **Usable on representative accounts.** Given representative test accounts, the finished system produces a result a real SDR would find usable — correct in direction, honest about uncertainty, free of fabricated detail.

These become real, enforced, testable checks incrementally: schema conformance starts Class 5, evidence citation Class 6–7, the full evaluation suite Class 9 (Book 1, Chapter 10).
