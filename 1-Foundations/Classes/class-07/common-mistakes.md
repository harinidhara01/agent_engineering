# Class 7 — Common Mistakes to Discuss (0:10–0:20)

Reviewing Class 6's homework before revealing `golden-solution/`.

## In the fabricated-evidence-reference diagnostic

- **A test that checks the field is non-empty but not that it's real.** The point of the diagnostic was realizing schema validation alone (`evidence_refs` is a non-empty list) cannot catch a reference to evidence that doesn't exist or doesn't support the claim. Watch for submissions that stop at "the list isn't empty" and call it solved.

## In the §7.8 extension (full seven-item tool test list)

- **Inventing a failure mode that doesn't actually fit the tool.** "Permission failure" forced onto a tool with no auth boundary sometimes produces a test that doesn't test anything real — for example, asserting a hardcoded `PermissionError` the code never actually raises. A good extension is honest that some categories require imagining a *future* version of the tool, not the current one.

## Talking points to set up today's class

- Ask: "Every tool so far reads from a file we control. What happens the first time the qualification agent needs a fact from outside WidgetWare entirely?" Let the room sit with that before revealing today's research pipeline.
- Preview the injection connection explicitly: "Remember Class 2's malicious account note? Today the same attack shows up in a source that looks like a real trade publication. Does that change how dangerous it is?"

## Golden solution reveal

Walk `class-06/`'s tools and contracts, then run `get_account_profile("acme-001")` live and ask: "This works because the data already lives in our repo. What would this function have to become if the account information genuinely didn't exist anywhere WidgetWare controls?" That question is today's entire class.
