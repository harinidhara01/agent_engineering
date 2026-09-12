# Class 4 Kahoot — 8 Questions

Run during 0:55–1:05. Correct answer marked with **✓**.

---

**1. (Terminology)** What is the difference between a Skill and a tool (§5.3)?
- A) They're interchangeable terms for the same thing
- **✓** B) A Skill tells the agent how to perform a task; a tool lets it do something outside the model
- C) A tool is written in Markdown; a Skill is written in Python
- D) A Skill requires network access; a tool never does

**2. (Terminology)** What is the difference between a Skill and a workflow (§5.4)?
- A) They're interchangeable terms for the same thing
- **✓** B) A Skill packages know-how one agent applies within a single reasoning step; a workflow coordinates multiple steps or agents over time
- C) A workflow is always faster than a Skill
- D) A Skill can only be used once per session; a workflow can be reused

**3. (Architecture)** Why does progressive disclosure (§5.6) matter for context consumption?
- **✓** A) A Skill can expose a concise discovery description and load full detail only when selected, reducing what's in the reasoning window
- B) It makes the Skill file smaller on disk
- C) It's required by ADK's `Agent` constructor
- D) It has no practical effect, only stylistic value

**4. (Architecture)** Why move the qualification procedure out of the agent's embedded instructions and into a Skill?
- **✓** A) So it becomes reusable, versioned, and independently testable, not locked inside one agent's Python file
- B) Because ADK's `Agent` class cannot accept long instruction strings
- C) Skills run faster than embedded instructions
- D) There's no real difference — it's purely cosmetic

**5. (Failure analysis)** The agent confidently qualifies an account with clearly insufficient evidence. Where's the fix — agent code or Skill procedure?
- **✓** A) The Skill procedure — the reasoning rules live there, not in `qualification_agent.py`
- B) The agent code, since that's where the model call happens
- C) Neither — this can only be fixed with structured outputs (Class 5)
- D) The context builder, since evidence lives there

**6. (Security/governance)** What does §5.7 say a Skill needs that "an anonymous prompt fragment" doesn't?
- **✓** A) A name, a version, and clear ownership — so changes to it can be reviewed like any other production asset
- B) Nothing — Skills and prompt fragments carry identical governance requirements
- C) Encryption at rest
- D) A dedicated model fine-tuned just for that Skill

**7. (WidgetWare scenario)** A second agent needs the same qualification logic. What does the Skill's reusability buy you here?
- **✓** A) Both agents share one maintained procedure instead of two copies that can silently drift apart
- B) Nothing — every agent needs its own copy of the logic regardless
- C) It means the second agent doesn't need a model at all
- D) It automatically merges both agents into one

**8. (Connecting back)** How does §3.5's evidence-policy vocabulary (Class 2) show up inside the Skill's procedure?
- **✓** A) The Skill's quality criteria explicitly require distinguishing fact from inference and never fabricating account attributes — the same categories Class 2 defined
- B) It doesn't — evidence policy only applies to Chapter 8's research pipeline
- C) The Skill replaces the evidence policy entirely
- D) Evidence policy only becomes relevant once tools are added in Class 6

---

## Facilitator notes

- Question 5 is worth pausing on — it's the first time the class has to locate a bug in the *right* file, and "Skill procedure, not agent code" is a distinction participants will keep needing through Class 9.
- Question 6 pairs well with a concrete example: ask what would happen if two engineers each independently "fixed" a copy-pasted procedure string differently, versus one owned Skill file with a changelog.
