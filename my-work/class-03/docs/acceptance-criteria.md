# Class 3 Acceptance Criteria — WidgetWare SDR Context Package

To achieve completion of Class 3, the project must satisfy all of the following observable acceptance criteria:

1. **Configuration Files**:
   - `config/products.yaml` exists and defines at least two offerings with approved claims.
   - `config/icp.yaml` exists with numeric size thresholds, preferred/excluded industries, preferred regions, and buying signals.
   - `config/policies.yaml` exists with the 5 evidence classifications (`verified_fact`, `derived_fact`, `inference`, `unknown`, `conflict`), prohibited actions, and human approval rules.

2. **System Instructions**:
   - `src/widgetware_sdr/instructions.py` exposes `get_system_instructions() -> str`.
   - Instructions mandate observable guidelines (factual backing, distinction between fact and inference, prohibiting invented facts/external actions).

3. **Context Builder**:
   - `src/widgetware_sdr/context_builder.py` exposes `build_context(account, objective, evidence, state=None) -> dict`.
   - Returns a structured dictionary preserving all 5 context layers (`system_instructions`, `business_context`, `task_context`, `retrieved_evidence`, `state`).
   - Ensures account data appears strictly within `task_context`.
   - Does not mutate input objects.
   - Defaults missing `state` to an empty dict `{}`.
   - Raises a descriptive error if required configuration YAMLs are missing.

4. **Evidence Provenance & Untrusted Data Isolation**:
   - Evidence records retain claim, classification, source name, source URL, retrieval date, and excerpt.
   - Account notes and retrieved text are treated as untrusted data and cannot alter system policies or authorize external actions.

5. **Scenario Fixtures**:
   - All 4 scenario YAMLs exist under `tests/scenarios/` (`qualified_account.yaml`, `unqualified_account.yaml`, `insufficient_evidence.yaml`, `prompt_injection.yaml`).

6. **Testing & Boundaries**:
   - Automated unit tests in `tests/unit/test_context_builder.py` pass cleanly (`pytest`).
   - Absolutely no ADK agent, LLM/Gemini calls, live web search, email sending, CRM integration, database persistence, or deployment logic exist.
