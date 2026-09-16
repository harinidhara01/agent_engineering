# Building Class 6 with Antigravity

Goal: give the agent its first real tools — three narrow, read-only functions for account, product, and ICP data, plus a deterministic fit-score helper kept outside model reasoning. `golden-solution/` in this folder is the reference. Build your own copy in `my-work/gemini-book-1/class-06/`, then diff.

## Prerequisites

- **`../SETUP.md` complete**, including a way to actually call Gemini if you want to observe real tool-calling behavior. Tool construction and unit testing are fully offline.
- Your Class 5 checkpoint, passing `./scripts/check.sh`.

## Steps

1. Ask Antigravity for the three tools, but review every line — tool descriptions are part of the contract with the model, not just documentation:

   > "Write three functions in `tools/account_data.py`: `get_account_profile(account_id: str)`, `get_widgetware_product(product_id: str)`, and `get_icp_policy()`. Each should have a docstring stating what it does, when to use it, and what it returns — the model selects tools by name and description alone, so be precise. Invalid input and a missing record should each return a dict with `error` and `error_category` keys, never raise an exception or fabricate a result."

2. Write `calculate_fit_score()` yourself, by hand, in `tools/fit_score.py` — it's pure arithmetic, and Book 1 §7 is explicit that this kind of calculation belongs outside model reasoning. Do not expose it to the agent as a tool; call it from application code only.

3. Update `qualification_agent.py`: attach the three read tools via `tools=[...]`, and add an explicit instruction telling the model to use them rather than assume account, product, or ICP facts from memory.

4. Write the tool tests independently of the agent (§7.8): valid input, invalid input, missing record, deterministic output shape, for each tool. Be honest in your own `KNOWN_FAILURE_CASES.md` about which of §7.8's seven categories genuinely don't apply yet (dependency failure, permission failure, redaction) versus which you're just skipping.

5. If you have credentials, run one live scenario and inspect the tool-call sequence in the returned events — confirm the agent actually calls `get_account_profile` before reasoning about employee count, rather than guessing.

## Verify

```
cd my-work/gemini-book-1/class-06
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
./scripts/check.sh
```

Expect all tool and contract tests to pass offline; integration tests skip without credentials.

## Compare against the reference

`golden-solution/tests/unit/test_tools.py` is the reference for what "independent of the agent" testing looks like — in particular, check that your tool tests never construct an `Agent` or call a model at all. If a tool test imports `qualification_agent`, it's testing the wrong thing.

## Grade it

Passing tests proves the tools return the right shape. It doesn't prove the tool descriptions are actually good enough for a model to select correctly, or that evidence references genuinely trace back to real tool calls. Run the quality check: `GRADING.md` in this folder plus `../GRADING-RUBRIC-TEMPLATE.md`.
