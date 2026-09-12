# Class 6 — Tool Engineering

**Manuscript source:** Book 1, Chapter 7 — Tool Engineering
**Seven-Step mapping:** Primary: Design Agent Capabilities / Supporting: Build the Harness, Evaluate & Govern
**Golden solution produced:** `class-06/golden-solution/`
**Starting checkpoint:** `class-05/golden-solution/`

## 0:00–0:20 — Homework review, common mistakes, golden solution reveal

- **Review homework:** ask participants to show their extra business invariant and explain, in one sentence, what real-world mistake it prevents.
- **Common mistakes to flag:** invariants tested only on the happy path with no failing-case counterpart; `BLOCKED` errors that are technically non-empty but not actually useful for debugging.
- **Golden solution reveal:** walk `class-05/`'s agent, print a valid `QualificationResult`, then ask: "Every fact in here — the employee count, the industry — where did the agent actually get it from?" (Answer: it's still trusting whatever's in the per-call message, exactly as it has since Class 3. It has no way to go look anything up itself. That's today's gap.)

## Slide outline (0:20–0:45)

1. Current WidgetWare state: a validated contract, but an agent that still can't reach outside what it's handed
2. Today's dependency: Class 5's `QualificationResult` and `EvidenceItem` contracts don't change structurally — tool-retrieved facts just start giving `evidence_refs` something real to point at
3. Business objective: an agent that retrieves its own facts instead of trusting whatever the caller hands it
4. Core concept: a tool lets the agent *do something outside the model* (§7.1) — the second of the three capability primitives after Skills
5. Terminology: tool descriptions are part of control (§7.2) — the model selects tools by name and description alone
6. Architecture: three narrow, read-only tools (§7.3) — `get_account_profile`, `get_widgetware_product`, `get_icp_policy`
7. Seven Steps mapping: Design Agent Capabilities continues — a tool is a capability engineered from the opposite direction of a Skill
8. Gemini vs. deterministic code: the model decides *when* to call a tool; `calculate_fit_score()` is pure arithmetic and never exposed as a callable tool at all
9. Security: least privilege for tools (§7.5) — a read-only lookup should never hold write-capable credentials, even if the underlying platform account technically could
10. Today's increment: `tools/account_data.py`, `tools/fit_score.py`, agent updated with `tools=[...]` and an instruction to use them instead of assuming facts
11. Lab architecture: tool testing without the agent (§7.8) — valid input, invalid input, missing record, deterministic output shape, tested completely independent of any model call
12. Acceptance criteria: every tool-retrieved fact used in a qualification result carries a real evidence identifier the tool actually returned

## Kahoot (8 questions)

- Terminology: What is the difference between a Skill and a tool (§7.1 recap of §5.3)?
- Terminology: Why does a tool's description matter as much as its implementation (§7.2)?
- Architecture: Why is `calculate_fit_score()` deterministic code and never exposed to the model as a callable tool?
- Architecture: What should `get_account_profile` return for a missing record — an exception, `None`, or something else (§7.4)?
- Failure analysis: The agent calls `get_widgetware_product` with a malformed `product_id` — what should happen, and where does that get tested?
- Security/governance: What does "permissions narrower than the underlying platform account" mean for a read-only tool (§7.5)?
- WidgetWare scenario: A `QualificationResult`'s `evidence_refs` entry doesn't trace to any tool-returned fact — what's wrong, and which layer should have caught it?
- Connecting back: How does §7.8's tool-testing checklist relate to the fail-safe pipeline Class 5 built for `parse_qualification_result`?

## Build together (0:55–1:35)

- `tools/account_data.py` — `get_account_profile`, `get_widgetware_product`, `get_icp_policy`, each read-only with typed `error`/`error_category` returns on failure
- `tools/fit_score.py` — `calculate_fit_score()`, deterministic, application-code-only, never in the agent's `tools=[...]` list
- update `qualification_agent.py`: attach the three tools, add an explicit "use these tools, don't assume facts" instruction

## Test and diagnose (1:35–1:50)

1. Run each tool's independent test suite (valid input, invalid input, missing record) with the agent entirely out of the picture.
2. Run one live scenario (with credentials) and inspect the tool-call sequence: did the agent call `get_account_profile` before reasoning about employee count, or did it guess?
3. Trigger a deliberate failure: call a tool with a malformed argument and confirm it returns a typed error, never raises.
4. Diagnose using the Framework's seven categories — this class's failures are almost always **tool implementation**, rarely context (that was Class 2's job) or contract (Class 5's).
5. Apply the smallest fix — usually a tool's output normalization, not a rewrite of the agent's instruction.
6. Re-run all tool and contract tests together.

## Homework

| Level | Task |
| ----- | ---- |
| **Required** | Build the three tools and `calculate_fit_score()`, attach the three read tools to the agent, and confirm the agent's qualification results now carry real, traceable evidence references |
| **Diagnostic** | A provided test case has a `QualificationResult` with `status=QUALIFIED` and an `evidence_refs` entry that doesn't actually correspond to any tool-returned fact — it was invented. Write a test that would catch a fabricated evidence reference, and explain in one sentence why the contract layer alone (Class 5) can't fully solve this |
| **Extension** | Pick one tool and write the full seven-item test list from §7.8, including the three this checkpoint's own tests skip (dependency failure, permission failure, redaction of prohibited fields) — invent a plausible way each could apply even though this checkpoint's tools don't currently have that failure mode for real |

- **Starting checkpoint:** `class-05/golden-solution/`
- **Files participants may modify:** `src/widgetware_sdr/tools/`, `src/widgetware_sdr/agents/qualification_agent.py`, `tests/`
- **Expected behavior:** every decisive claim in a qualification result carries an evidence reference traceable to an actual tool call, not an assumed fact
- **Tests that must pass:** all tool tests, all prior contract tests
- **Submission:** one full `QualificationResult` JSON output for the Acme account, with `evidence_refs` populated and traceable
- **Constraints:** tools remain read-only — no send action, no CRM write, still Book 1's standing boundary from Class 1; `calculate_fit_score()` must never be exposed to the model as a callable tool

## Golden solution: `class-06/`

Adds the three tools and `calculate_fit_score()` on top of `class-05/` without changing the contracts' structure. README notes: "This checkpoint gives the agent its first real tools: three narrow, read-only functions for account, product, and ICP data, plus a deterministic fit-score helper kept outside model reasoning."

## Bridge to Class 7

Class 7 takes the agent outside WidgetWare's own trusted data for the first time — evidence-backed external research through MCP, where retrieved content must be treated as untrusted until validated.
