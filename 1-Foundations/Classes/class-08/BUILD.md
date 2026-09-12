# Building Class 6 with Antigravity

Goal: compose the Research and Qualification agents plus two new ones (Evidence Reviewer, Drafting Agent) into one coordinated workflow, with an explicit state machine and a human approval gate no code path can bypass. `golden-solution/` in this folder is the reference. Build your own copy in `my-work/gemini-book-1/class-08/`, then diff.

## Prerequisites

- **`../SETUP.md` complete.**
- Your Class 5 checkpoint, passing `./scripts/check.sh`.

## Steps

1. Write `workflow/state_machine.py` yourself, by hand, before anything else — draw the ten states and their legal transitions on paper first. This is the one file in the whole course most worth writing without an AI's help on the first pass, because getting the transition table right *is* the exercise.

2. Confirm, explicitly, that no state in your enum could mean "sent" — write the test for this before writing anything else.

3. Write `workflow/approval.py`: `ApprovalPackage` (the fields Book 1 §9.6 requires) and `record_approval_decision()`, which returns a state, never performs an action.

4. Ask Antigravity for the two new agents, but review the instructions closely — this is where the chapter's real safety property lives:

   > "Write `agents/evidence_reviewer.py`, an ADK agent with no tools. Its instruction must require it to verify claims are cited and current, surface any conflicts rather than resolving them, and explicitly forbid independently browsing for additional facts. Write `agents/drafting_agent.py`, also with no tools, whose instruction restricts it to only the claims it's given — it must never introduce a fact not present in its input."

5. Write `workflow/coordinator.py`'s `run_workflow()` yourself. Design it to accept `qualify`, `review`, and `draft` as parameters (plain callables) rather than calling specific agent objects directly — this is what makes the coordinator testable without a live model call, and it's a real, defensible software-engineering pattern (dependency injection), not a shortcut. Checkpoint after every stage.

6. Write the five required scenario tests using simple stub functions for `qualify`/`review`/`draft` that return pre-built contract objects: success, insufficient evidence, source conflict, malformed output (a stub that raises), rejected approval.

7. Write a checkpoint test that actually reads a checkpoint file back and confirms the state and history are correct.

## Verify

```
cd my-work/gemini-book-1/class-08
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
./scripts/check.sh
```

All workflow, state-machine, and contract tests should pass offline.

## Compare against the reference

`golden-solution/tests/workflow/test_state_machine.py`'s `test_sent_is_not_a_state_that_exists` and `test_terminal_states_have_no_outgoing_transitions` are the reference for what "structurally cannot send" actually means here — not a comment, not a docstring, a test that would fail if someone added a `SENT` state later without noticing what they'd done.

## Grade it

Passing tests proves the state machine and checkpointing are correct, using stub agent functions. It doesn't prove the real Evidence Reviewer and Drafting Agent behave correctly with a live model. Run the quality check: `GRADING.md` in this folder plus `../GRADING-RUBRIC-TEMPLATE.md`.
