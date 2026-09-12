# ADR 0001: Bound autonomy at "Prepare," not "Execute"

## Status

Accepted.

## Context

WidgetWare SDR Lab could plausibly be built at several points on the autonomy spectrum — from a system that only answers questions about a company, up to one that researches, qualifies, drafts, and sends outreach entirely on its own. A higher autonomy level is not automatically more advanced; it is more consequential, and it requires more of everything else to be trustworthy first: evaluation, identity, audit trails, a human owner who can actually intervene.

## Decision

Book 1 implements autonomy level 4 — **Prepare**: the system researches, recommends a qualification, drafts outreach, and assembles a complete approval package for a person. It does not implement level 5 (**Execute with approval**) or beyond. This decision holds for the entire book, not just this checkpoint.

## Alternatives considered

- **Level 3 (Draft only), no approval package** — rejected. A draft with no structured handoff to a human reviewer just shifts the qualification-judgment work back onto the person with less support than the system could have given them.
- **Level 5 (Execute with approval)** — rejected for Book 1. This would require an actual send-capable tool gated by an approval check the model cannot bypass. Building that safely requires the contracts, workflow state machine, and evaluation discipline that don't exist until much later in the course — building the send tool before those exist would mean shipping the risky capability before the controls around it.
- **Level 7 (open-ended)** — never seriously considered. Nothing about WidgetWare's business problem calls for a system that selects its own targets, channels, or strategies.

## Consequences

- No chapter or class in Book 1 ever adds a send-capable tool. This is a standing constraint on every future class's scope, not a preference.
- The approval package (evidence, draft, risk flags) has to be genuinely usable by a person, since it is the terminal artifact of the entire system for now — there is no "it'll get better once it can send on its own" escape valve.
- Autonomy expansion, if it ever happens, is Book 2 territory at the earliest, and would need its own explicit ADR, evaluation evidence, and identity/audit story — not a quiet capability addition.
