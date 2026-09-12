# Class 4 — Common Mistakes to Discuss (0:00–0:30)

Reviewing Class 3's homework before revealing `golden-solution/`.

## In the diagnostic (boundary-condition test)

- **A boundary test that checks the number but not the label.** Class 3's extension asked for an account at exactly 5,000 employees — the ICP minimum itself. A submission that gets the qualification outcome right but never actually asserts *why* (an explicit "at least" vs. "more than" comparison) hasn't proven the boundary is handled on purpose rather than by accident.

## In the required build (embedded procedure)

- **Procedure text that reads well but hides an ambiguity at the threshold.** The most common version of this: "significant headcount" without ever stating the number, leaving the model to guess where the line is — which defeats the point of writing the procedure down at all.

## Talking points to set up today's class

- Ask: "If a second agent needed this exact same qualification reasoning, what would you have to do right now?" — the expected answer is "copy-paste the string," which is exactly the problem today solves.
- Preview progressive disclosure before revealing it: ask what happens to context consumption if every Skill's full procedure loaded for every agent call, all the time, whether or not that Skill was actually relevant.

## Golden solution reveal

Run `class-03/`'s agent live once, and print its assembled instruction. Highlight where the qualification procedure sits — inline, as a Python string. Then ask: "What breaks if WidgetWare adds a second agent that needs this same logic?" (Answer: nothing breaks immediately, but the two copies will drift the first time either one changes. That's the whole gap this class closes.)
