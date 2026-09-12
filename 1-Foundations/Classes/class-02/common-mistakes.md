# Class 2 — Common Mistakes to Discuss (0:10–0:20)

Reviewing Class 1's homework before revealing `golden-solution/`.

## In `scripts/check.sh` / the one-command check

- **A check script that only runs tests, not lint or format.** Participants sometimes narrow "all baseline checks" to "the tests pass," quietly dropping the lint/format half. Ask them to run `./scripts/check.sh` live and confirm all three steps actually execute, not just the last one.
- **A health check that isn't actually deterministic.** Watch for a health-check function that reads an environment variable with no default, so it passes on the author's machine and fails on a clean clone — exactly the "can a stranger clone this and get a clean pass" criterion from Class 1's homework.

## In the Antigravity gap-report exercise

- **A "gap" that's really just a missing README instruction, not a missing capability.** The point of the exercise is realizing documentation gaps *are* real gaps — participants sometimes dismiss these as too minor to fix. Push back gently: an undocumented setup step is exactly the kind of thing that costs the next person an hour.

## In repository instructions (Extension homework)

- **Instructions that are aspirational rather than checkable** — "write good tests" instead of "every behavior change ships with at least one new or updated test in the same commit." This is the same failure pattern as Class 1's non-testable acceptance criteria, recurring in a new place.

## Talking point to close the segment

Today's chapter is going to ask you to build something that looks unglamorous — YAML files and one assembly function — and insist that it's actually the most important class in the book so far. The common thread in this review is: every mistake above is something that would have silently gotten worse the moment we added a context layer on top of it. That's exactly why we're fixing workspace hygiene before touching Gemini at all.
