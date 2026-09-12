# How to Work a Class (Self-Paced Track)

The generic procedure for working through any class in the Gemini edition of this book on your own, from first fork through grading. Every class's own `BUILD.md` assumes you've read this once.

This is the self-paced counterpart to the classroom cadence in `00_Course_Framework.md`. If you're in the live, instructor-led program, you don't need this file.

## One-time setup

1. **Fork** the companion repository, [github.com/sensei-ji/agent_engineering](https://github.com/sensei-ji/agent_engineering.git), on GitHub into your own account.
2. **Clone your fork** locally and track the original as `upstream`:

   ```
   git clone <your-fork-url>
   cd agent_engineering
   git remote add upstream https://github.com/sensei-ji/agent_engineering.git
   ```

3. **Install tools** per `SETUP.md` — Antigravity, Git, Python 3.11+. This happens once, before Class 1, precisely so Class 1's own exercise — drafting the charter *and* standing up the runnable repository harness — isn't also an installation tutorial.

## Per class-0N

4. **Sync your fork** before starting, in case earlier classes were fixed or new ones published:

   ```
   git fetch upstream
   git merge upstream/main
   git push origin main
   ```

5. **Copy the previous class's golden solution**, not class-0N's own, into `my-work/` as your starting point:

   ```
   cp -r 1-Foundations/Classes/class-0(N-1)/golden-solution/ \
         my-work/gemini-book-1/class-0N/
   ```

   `class-0N/golden-solution/` in the repo is the finished reference solution — don't open it yet. (Class 1 has no predecessor; start from its own `BUILD.md` directly, working in a scratch directory rather than `my-work/`, since there is no prior checkpoint to copy forward yet.)

6. **Read the manuscript chapter** (`../Manuscript/0N_Chapter_...md`) for the concept, then work through `class-0N/BUILD.md` — but building inside `my-work/gemini-book-1/class-0N/`, not the reference folder.

7. **Gate check — run the tests.** From your working folder:

   ```
   cd my-work/gemini-book-1/class-0N
   python3 -m venv .venv && source .venv/bin/activate
   pip install -e ".[dev]"
   python3 -m pytest -q
   ```

   This is deterministic and binary: it checks the structural contract (files exist, schemas validate, required fields are present), not whether your solution is *good*. Don't skip it, but don't mistake it for step 9 either.

8. **Verify and fix** until every test passes.

9. **Now** open the gold solution (`class-0N/golden-solution/`) and diff against your own. Look at what you did differently, what you missed, and — just as importantly — where your approach is legitimately different but equally valid. The reference is one correct answer, not the only one.

10. **Quality check — LLM-as-judge.** Gate tests can't tell you whether your `context_builder.py` is well-isolated or your ICP config is internally coherent. Follow `GRADING-RUBRIC-TEMPLATE.md` together with `class-0N/GRADING.md` (that class's specific criteria) to have Antigravity (or Gemini directly) grade your submission against the gold solution on the things pytest can't check.

11. **Commit** your working folder to your fork. Optionally open a PR against your own fork's main branch just to keep a record — there's no requirement to push it anywhere else.

## The two-tier testing model

Every class distinguishes two different kinds of "is this done":

| | Gate check (step 7) | Quality check (step 10) |
|---|---|---|
| Tool | `pytest` | Antigravity/Gemini, as an LLM judge |
| Nature | deterministic, offline | subjective, rubric-guided |
| Answers | "Did you meet the contract?" | "Is it actually good?" |
| Failure mode if skipped | broken structure ships silently | shallow, copy-of-the-reference work passes unnoticed |

Passing gate tests is necessary but not sufficient. A `context_builder.py` that exists, assembles all four context layers, and passes every test can still isolate untrusted content weakly — that's what step 10 is for.

## How this relates to the classroom track

The classroom program (`00_Course_Framework.md`) uses the same `golden-solution/` per class as this track, and the same manuscript. It substitutes a live instructor build, Kahoot checks, and informal homework review for this track's self-directed `BUILD.md` and LLM-judge grading. Neither track is the "real" one — they're two ways of using the same underlying material.
