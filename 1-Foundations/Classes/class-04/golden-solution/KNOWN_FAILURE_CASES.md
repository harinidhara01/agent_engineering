# Known Failure Cases — Class 4 Checkpoint

## Carried forward from Classes 1–2

- `expected_qualification_direction`/`rationale` in fixtures are still hand-derived, now finally checkable by a real agent — but only when live credentials are present (see #1 below).
- Business-config drift between `config/icp.yaml` and `tests/fixtures/expected/*.yaml` is still undetected by any test.
- The three scenario accounts remain illustrative, not a representative dataset.

## New at this checkpoint

### 1. The three semantic scenario tests are skipped by default in this environment

`tests/integration/test_qualification_agent_live.py` requires `GOOGLE_API_KEY` or a configured Vertex AI project. Without one, `pytest` reports these as **skipped**, not passed — do not mistake a clean `17 passed, 3 skipped` run for proof the agent reasons correctly. The 17 passing tests only prove the agent *constructs* correctly (right model, right instruction content, no leaked account data, no tools yet). Whether it actually avoids inventing an employee count or correctly explains a `NEEDS_RESEARCH` outcome is unverified until someone runs the integration suite with real credentials.

### 2. `data/sample_accounts/` and `tests/fixtures/accounts/` are duplicated, not shared

Book 1 §4's Hands-on Lab asks for sample account profiles under `data/sample_accounts/`, and this checkpoint already had `tests/fixtures/accounts/` from Class 2. Rather than pick one, this checkpoint keeps both, with identical content, for two different audiences (`data/` for someone exploring the agent locally; `tests/fixtures/` for the test suite). They are not read from a single source — if one is edited without the other, they will silently drift. A future class could fix this properly with a single source of truth; this checkpoint does not.

### 3. `build_agent_instruction()` re-reads and re-renders YAML on every call

There is no caching. For a single local run this is invisible; at any real scale (Book 2, once many requests happen concurrently), rebuilding the full instruction string — including a full skill.md read — on every single agent construction is wasteful. Not fixed here; flagged for Book 2's context-engineering-at-scale material.

### 4. The agent's prose output format (`QUALIFY` / `DO_NOT_QUALIFY` / `NEEDS_RESEARCH`) is not yet validated

Nothing in this checkpoint checks that the model's response actually uses one of these three exact tokens, or in what format. That's precisely the gap Class 5 (Book 1 Chapter 6, structured outputs) exists to close — this checkpoint's output is still free-form prose, exactly as intended, but it means a subtly malformed or off-format response would currently go undetected by any test here.
