#!/usr/bin/env python3
"""Targeted tests for the skill stability frontmatter helper."""

import sys
from pathlib import Path

SKILLS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILLS_DIR))

from stability import (  # noqa: E402
    VALID_STABILITY,
    parse_frontmatter,
    read_stability,
    validate_skill_dir,
    validate_stability,
)


def test_valid_enum_values():
    assert VALID_STABILITY == ("experimental", "stable", "deprecated")


def test_parse_frontmatter_strips_quotes_and_ignores_comments():
    text = '---\nname: "x"\nstability: "stable"\n# comment\n---\n# Heading\n'
    fields = parse_frontmatter(text)
    assert fields == {"name": "x", "stability": "stable"}


def test_parse_frontmatter_without_fences_is_empty():
    assert parse_frontmatter("# Heading\nstability: stable\n") == {}


def test_demo_skills_declare_valid_stability():
    expected = {
        "stability-demo": "stable",
        "experimental-demo": "experimental",
        "deprecated-demo": "deprecated",
    }
    for name, value in expected.items():
        assert read_stability(SKILLS_DIR / name / "SKILL.md") == value
        assert validate_skill_dir(SKILLS_DIR / name) == []


def test_missing_stability_field_is_reported(tmp_path):
    skill = tmp_path / "SKILL.md"
    skill.write_text("---\nname: \"x\"\n---\n# Heading\n", encoding="utf-8")
    errors = validate_stability(skill)
    assert len(errors) == 1
    assert "missing required 'stability'" in errors[0]


def test_invalid_stability_value_is_reported(tmp_path):
    skill = tmp_path / "SKILL.md"
    skill.write_text("---\nstability: \"beta\"\n---\n", encoding="utf-8")
    errors = validate_stability(skill)
    assert len(errors) == 1
    assert "invalid stability 'beta'" in errors[0]


def test_missing_file_is_reported(tmp_path):
    errors = validate_stability(tmp_path / "nope.md")
    assert len(errors) == 1
    assert "file not found" in errors[0]


if __name__ == "__main__":
    import pytest

    raise SystemExit(pytest.main([__file__, "-v"]))
