# ADR 0002: No outbound send capability exists in code, anywhere in Book 1

## Status

Accepted.

## Context

ADR 0001 bounds the system's *permitted* autonomy at "Prepare." That alone is a policy decision — the kind of thing that could, in principle, be enforced by a runtime check that inspects an approval flag before allowing a send. A policy check is real protection, but it is protection that depends on every future line of code correctly calling it, forever.

## Decision

WidgetWare SDR Lab contains no send-capable function, no outbound email or messaging client, and no tool a model could invoke to transmit anything outside this repository's own process — not gated behind an unused flag, not stubbed out, not present-but-disabled. The guarantee is structural: the capability does not exist in code, so there is nothing for a policy check, a prompt, or a misconfiguration to accidentally unlock.

## Alternatives considered

- **Build a send tool, gate it behind an approval check** — rejected for Book 1. This is a real, defensible pattern for a mature system, but it makes the guarantee only as strong as every call site's discipline about checking the gate. A structural absence is strictly stronger, and Book 1's job is to teach the discipline of proving that kind of guarantee, not just asserting it.
- **Build a send tool that always fails in this environment (e.g., no configured credentials)** — rejected. This is security by missing configuration, not security by design. A misconfigured or copy-pasted environment could accidentally make it work.

## Consequences

- Every class's `KNOWN_FAILURE_CASES.md` and acceptance criteria can state "no autonomous send" as a claim verifiable by *inspecting the codebase for the absence of a capability*, not by trusting that a check fires correctly at runtime.
- If a future exercise or homework assignment asks a learner to "add a send tool," that assignment is out of scope for Book 1 and should be flagged, not completed.
- This ADR is binding on every class in this course, not just Class 1 — a later class that quietly adds outbound-send capability would violate this decision, not just extend the system.
