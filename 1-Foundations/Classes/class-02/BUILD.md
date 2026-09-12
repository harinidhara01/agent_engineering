# Building Class 2 with Antigravity

Goal: a deliberate context architecture — WidgetWare's business rules as data, fixed system instructions, and a context-assembly pipeline that keeps account-supplied content structurally isolated from system policy. Still no model call anywhere in this codebase. `golden-solution/` in this folder is the reference. Build your own copy in `my-work/gemini-book-1/class-02/`, then diff.

## Prerequisites

- **`../SETUP.md` complete.**
- Your Class 1 workspace, working and passing `./scripts/check.sh` (or `../class-01/golden-solution/` if you didn't do the self-paced Class 1).

## Steps

1. Start from your Class 1 checkpoint. Confirm `./scripts/check.sh` passes before adding anything — Class 2 adds a new dependency (`PyYAML`) and new tests, and it will be much harder to tell new failures from old ones if you start broken.

2. Ask Antigravity to draft the three business-configuration files, giving it the actual facts rather than letting it invent them:

   > "Create `config/products.yaml`, `config/icp.yaml`, and `config/policies.yaml` for WidgetWare. WidgetWare sells software that helps manufacturing and industrial-automation companies modernize plant operations and adopt AI-enabled automation. The ICP: minimum 5,000 employees, no upper bound, preferred industries manufacturing and industrial_automation, excluded industries financial_services/healthcare/retail, preferred regions united_states/europe/india, buying signals new_ai_leadership/digital_transformation_program/genai_hiring. Policies should list the five evidence categories (verified_fact, derived_fact, inference, unknown, conflict), prohibited actions, and an escalation rule: insufficient evidence must produce NEEDS_RESEARCH rather than a guess."

3. Write `src/widgetware_sdr/instructions.py` yourself, by hand, before asking Antigravity for help — this file is short, and the discipline of writing fixed system instructions without letting any account data leak into them is the entire point of the chapter. It should centralize model selection (read from an environment variable, with a default) and define a `SYSTEM_INSTRUCTIONS` constant covering role, scope, evidence requirements, how to treat untrusted content, and prohibited actions.

4. Now the context builder. Ask Antigravity for a first draft, then read every line before accepting:

   > "Write `src/widgetware_sdr/context_builder.py`. It should build a `ContextPackage` from an account dict and optional notes, combining: fixed system instructions (imported, never derived from account data), business context (loaded from the three YAML files), task context (the account and workflow stage), and evidence (each note wrapped as an `EvidenceItem` with `origin` and `trust` fields, always `untrusted`). The assembled prompt must render system instructions first, business and task context next, and all evidence last, inside clearly delimited `BEGIN EVIDENCE`/`END EVIDENCE` markers — in that fixed order, every time."

5. Write the four required context tests yourself: a clearly qualified account, a clearly unqualified account, an account with insufficient evidence, and a malicious note. Build the malicious-note test last, and deliberately run it before you're confident the delimiting is correct — watch it fail, then fix `context_builder.py` until it passes. Seeing the failure mode matters more than skipping straight to green.

   The malicious-note test should assert two separate things, not one: that the injected text is present somewhere in the assembled prompt (you don't silently drop real input), and that it appears strictly *after* the `BEGIN EVIDENCE` marker — never before or inside the instructions or business-context sections. Presence alone is a weaker test than position.

6. Optional but recommended: pull your test accounts into `tests/fixtures/accounts/*.yaml` and `tests/fixtures/expected/*.yaml` instead of hardcoding them inline, and load them in your tests. This is what Class 2's own golden solution does, and it's the difference between a test file that's also documentation and one that isn't.

## Verify

```
cd my-work/gemini-book-1/class-02
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
./scripts/check.sh
```

Expect 8 tests to pass (3 health-check, 5 context). Print the assembled context for at least one scenario and actually read it:

```
python3 -c "
from widgetware_sdr.context_builder import build_context
ctx = build_context({'account_id': 'acme-001', 'company_name': 'Acme Manufacturing', 'industry': 'manufacturing', 'employee_count': 22000, 'region': 'united_states'})
print(ctx.assembled_prompt)
"
```

If you can't hold the whole thing in your head while reading it top to bottom, it's already too big.

## Compare against the reference

`golden-solution/tests/unit/test_context_builder.py` is the reference. Pay particular attention to how its malicious-note test asserts on section *ordering* (`instructions_index < evidence_begin_index < malicious_index`), not just text presence — if yours only checks presence, strengthen it.

## Grade it

Passing tests proves the context assembles and stays structurally isolated. It does not prove the isolation is actually robust, or that your system instructions are well-written. Run the quality check: `GRADING.md` in this folder plus `../GRADING-RUBRIC-TEMPLATE.md`.
