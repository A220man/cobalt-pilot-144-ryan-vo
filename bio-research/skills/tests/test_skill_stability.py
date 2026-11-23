#!/usr/bin/env python3
"""Targeted test for stability lifecycle frontmatter in skills."""

import os

STABILITY_VALUES = {"experimental", "stable", "deprecated"}
SKILLMD_FILENAME = "SKILL.md"


def _read_skillmd(skill_dir: str) -> str:
    """Read SKILL.md from a skill directory, return raw text."""
    path = os.path.join(skill_dir, SKILLMD_FILENAME)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _extract_frontmatter(content: str) -> dict:
    """Extract frontmatter from SKILL.md.

    Format: starts with --- delimiter, frontmatter fields (key: value)
    continue until the first # heading line.
    """
    # Remove leading --- if present
    if content.startswith("---"):
        content = content[3:]
    # Find the first # heading line
    for i, line in enumerate(content.splitlines()):
        stripped = line.strip()
        if stripped.startswith("#"):
            # Frontmatter is everything before this line
            frontmatter_text = "\n".join(content.splitlines()[:i])
            break
    else:
        # No # heading found, take all
        frontmatter_text = content
    
    fields = {}
    for line in frontmatter_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip()
            # Remove surrounding quotes (single or double)
            if (value.startswith('"') and value.endswith('"')) or \
               (value.startswith("'") and value.endswith("'")):
                value = value[1:-1]
            fields[key] = value
    return fields


def test_stability_field_exists_in_skill_demo():
    """SKILL.md schema includes stability field with enum values."""
    skill_dir = os.path.join(
        os.path.dirname(__file__), "..", "stability-demo"
    )
    content = _read_skillmd(skill_dir)
    fields = _extract_frontmatter(content)
    assert "stability" in fields, (
        f"SKILL.md in stability-demo must have a 'stability' frontmatter field. "
        f"Found fields: {list(fields.keys())}"
    )


def test_stability_field_valid_value():
    """Stability field value must be one of experimental|stable|deprecated."""
    skill_dir = os.path.join(
        os.path.dirname(__file__), "..", "stability-demo"
    )
    content = _read_skillmd(skill_dir)
    fields = _extract_frontmatter(content)
    stability = fields.get("stability", "")
    assert stability in STABILITY_VALUES, (
        f"stability='{stability}' is not a valid value. "
        f"Must be one of {STABILITY_VALUES}"
    )


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
