# Class 5 Grading Criteria

Used with `../GRADING-RUBRIC-TEMPLATE.md`. These are the criteria specific to this class — the things `pytest` cannot check, or can only check for the specific cases already anticipated.

1. **Conflict detection's actual scope is documented honestly.** A submission's own notes (README, `KNOWN_FAILURE_CASES.md`, or code comments) should say plainly what pattern the detector actually catches, not imply it "handles conflicting sources" in general. If a submission's conflict detector is broader than this course's reference, that's a legitimate improvement — but it should still be documented precisely, not left for a reader to reverse-engineer.

2. **The injection-attempt test proves isolation, not just survival.** A test that only confirms `build_research_brief` doesn't crash on injection-laden input is weaker than one that confirms the attack text ends up as ordinary, cited claim data — exactly where any other evidence text would land, no special handling, no special exception.

3. **The choice of function tool vs. MCP is argued, not assumed.** A strong submission states which of §8.5's four conditions actually applied to this specific research source, and reaches a defensible conclusion — even if that conclusion is "MCP would be better here, but a function tool is simpler for a course lab."

4. **`ResearchBrief`'s claims are genuinely tied to evidence, not decoratively.** Pick one claim in a generated brief and trace its `evidence_refs` back to a real evidence item's `claim` text. If the two don't actually match — the claim says something the cited evidence doesn't support — the citation is present but hollow.

5. **The Research Agent's instruction would plausibly work on a model that's never seen this codebase.** Read it as an outsider. Does it clearly say what to do when evidence conflicts, and what never to do with retrieved text — without relying on context only the course provides?

6. **Independent understanding, not a copy.** If the submission's mock data, pipeline, and Research Agent are near-identical to the gold reference in wording and structure with no evidence of independent construction, note that explicitly per the anti-gaming guidance in the generic template.
