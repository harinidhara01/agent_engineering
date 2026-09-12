# Class 10 — Common Mistakes to Discuss (0:00–0:20)

Reviewing Class 9's homework before revealing `golden-solution/`.

## In the required build (golden dataset and release gate)

- **A golden-dataset case that's present but doesn't actually cover a real failure mode.** Ten cases satisfies the letter of "cover all required categories," but a case that could never actually fail — because its expected outcome is trivially true regardless of the code — isn't testing anything. Ask participants to name what specifically would have to break for each of their cases to fail.

## In the diagnostic (release gate reporting every failure)

- **A fix that reports two failures but only because they happened to be checked independently already.** The point of the diagnostic was removing an early-return or short-circuit; a submission that "fixes" it by adding a second, parallel check path without removing the original short-circuit may only work for this specific test case, not the general one.

## Talking points to set up today's class

- Ask: "We proved the workflow is trustworthy for one account, run once, on request. What happens the moment WidgetWare hands you a hundred accounts and goes home for the night?" Let the room sit with the gap before revealing today's loop.
- Preview the five-way decision before revealing it: ask what should happen when an account has failed twice already and fails a third time. Most will say "give up" — introduce ESCALATE as the more honest answer: hand it to a person, don't just discard it.

## Golden solution reveal

Run Class 9's release gate live against the Class 9 checkpoint and watch it pass. Then ask: "This proves one run is trustworthy. Prove it to me for a hundred runs, overnight, with nobody watching." That question is today's entire class.
