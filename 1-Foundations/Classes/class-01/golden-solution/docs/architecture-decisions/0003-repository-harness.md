# ADR 0003: Build the repository harness in Class 1, not deferred to a later class

## Status

Accepted. (Supersedes the previous course structure, in which the harness was Class 2's entire topic and Class 1 produced no runnable code at all.)

## Context

The original eleven-class structure treated "frame the use case" (charter, specification, business brief) and "build the harness" (installable package, health check, quality gate) as two separate classes, in that order, with Class 1 producing no code whatsoever. That ordering has a real pedagogical rationale — Frame the Use Case genuinely is a discipline independent of any implementation technology, and demonstrating that with zero code is a legitimate teaching choice.

In practice, it also meant the course's first checkpoint was not runnable, not verifiable by an automated test, and not something a learner could confirm they'd completed correctly except by comparing prose against prose. Every class after it, by contrast, is judged by a deterministic gate plus a qualitative review. Class 1 was the one exception, and it stayed the exception for an entire class's worth of material.

## Decision

Merge the former Class 1 (charter) and Class 2 (harness) into a single revised Class 1. The revised checkpoint keeps every charter artifact from the original Class 1 — business brief, specification, acceptance criteria, scenarios — and adds the installable package, deterministic health check, environment verification, and one-command quality gate that used to be Class 2's entire scope.

The result: Class 1 is the first runnable, reproducible, known-good baseline. Every class from the revised Class 2 onward starts from it exactly the way classes previously started from Class 2's checkpoint.

## Alternatives considered

- **Leave Class 1 as charter-only, keep the eleven-class structure** — rejected. This was the status quo; the whole point of this ADR is to change it.
- **Move the harness earlier but keep it a separate class, renumbering everything by one instead of merging** — rejected. This doesn't actually solve the problem (Class 1 would still be non-runnable); it just relabels which class has that property.
- **Fold the harness into Class 1 but keep Class 1 non-runnable, deferring `scripts/check.sh` to Class 2** — rejected. A charter without a way to mechanically verify anything about the surrounding repository isn't actually a different kind of checkpoint than before; it just has more prose.

## Consequences

- The course is now ten classes, not eleven — see the course framework's old-to-new class mapping for the full renumbering.
- Every reference to "Class 1 has no code" or "there is nothing to run yet" is now false and must be removed from course materials, not just softened.
- The manuscript's own two-chapter structure (Book 1, Chapters 1 and 2) is unchanged — this ADR is a course-delivery decision, not a manuscript decision. The book still teaches Frame the Use Case and Build the Harness as two chapters; the live course now teaches them together in one class, in one sitting, because doing so produces a strictly more useful first checkpoint without sacrificing either chapter's content.
