# Class 6 Kahoot — 8 Questions

Run during 0:45–0:55. Correct answer marked with **✓**.

---

**1. (Terminology)** What is the difference between a Skill and a tool (§7.1 recap of §5.3)?
- A) They're interchangeable terms for the same thing
- **✓** B) A Skill tells the agent how to perform a task; a tool lets it reach outside the model and act
- C) A tool is written in Markdown; a Skill is written in Python
- D) A Skill requires network access; a tool never does

**2. (Terminology)** Why does a tool's description matter as much as its implementation (§7.2)?
- **✓** A) The model selects tools based on their names and descriptions — a vague description leads to misuse regardless of how correct the code is
- B) Descriptions are only used for human documentation, never read by the model
- C) ADK requires descriptions to be under 10 words
- D) It doesn't — only the function signature matters

**3. (Architecture)** Why is `calculate_fit_score()` deterministic code and not a model judgment?
- **✓** A) It's a fixed, auditable arithmetic formula — exactly the kind of calculation that belongs outside model reasoning
- B) Because ADK does not allow tools to return numbers
- C) Because the model cannot perform arithmetic reliably at all
- D) There's no real reason; it could be either

**4. (Architecture)** What should `get_account_profile` return for a missing record (§7.4)?
- **✓** A) A typed dict with `error` and `error_category` keys — never an unhandled exception, never a fabricated result
- B) `None`, silently
- C) An exception the caller must catch
- D) A default, generic account profile

**5. (Failure analysis)** The agent calls `get_widgetware_product` with a malformed `product_id`. What should happen, and where does that get tested?
- **✓** A) The tool returns a typed error result, and this is tested completely independent of the agent per §7.8
- B) The model should catch the malformation itself before calling the tool
- C) The application should crash with a stack trace
- D) This can only be tested with live model credentials

**6. (Security/governance)** What does "permissions narrower than the underlying platform account" mean for a read-only tool (§7.5)?
- **✓** A) A read-only lookup tool should never hold credentials capable of a write, even if the platform account technically could
- B) The tool should have root access for convenience
- C) It refers only to file-system permissions, not data access
- D) It's a Book 2 concept — Book 1 tools don't need this yet

**7. (WidgetWare scenario)** A `QualificationResult`'s `evidence_refs` entry doesn't trace to any tool-returned fact. What's wrong, and which layer should catch it?
- **✓** A) The evidence was fabricated — Class 5's contract layer alone can't catch this, since it only checks the field is non-empty, not that its contents are real; that needs a semantic check
- B) Nothing is wrong — evidence references don't need to trace to anything
- C) The tool itself is broken
- D) This is expected and gets fixed automatically in Class 7

**8. (Connecting back)** How does §7.8's tool-testing checklist relate to the fail-safe pipeline Class 5 built for `parse_qualification_result`?
- **✓** A) Both apply the same principle at a different layer — malformed input should produce a typed, informative error, never a crash or a silent guess
- B) They're unrelated — tool testing has nothing to do with contract validation
- C) Tool testing replaces the need for contract validation
- D) §7.8 only applies once live credentials are available

---

## Facilitator notes

- Question 7 is the crux of the class — participants should leave understanding that a schema-valid contract doesn't guarantee semantically true content, and that's a gap no single layer fully closes on its own.
- Question 4 pairs well with a live demo: call `get_account_profile` with a nonexistent account ID and read the typed error result aloud.
