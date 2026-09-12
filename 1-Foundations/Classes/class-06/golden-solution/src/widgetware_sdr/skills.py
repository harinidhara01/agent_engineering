"""Load Skill procedures from the skills/ directory.

Book 1, Chapter 5: a Skill is a maintained, reusable procedure document —
not application code, and not embedded permanently inside one agent's
instructions. This module's only job is to read one into a string an
agent's instruction can include.
"""

from __future__ import annotations

from pathlib import Path

SKILLS_DIR = Path(__file__).resolve().parent.parent.parent / "skills"


def load_skill(name: str) -> str:
    """Return the procedure text of the named Skill's skill.md."""
    path = SKILLS_DIR / name / "skill.md"
    return path.read_text(encoding="utf-8")
