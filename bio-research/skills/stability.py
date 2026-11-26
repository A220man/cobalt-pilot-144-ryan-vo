"""Stability lifecycle frontmatter for skills (experimental/stable/deprecated).

A small, dependency-free helper for reading and validating the ``stability``
field declared in a skill's ``SKILL.md`` YAML frontmatter. Agents can use this
to filter skills by lifecycle status before invoking them.

Frontmatter format (YAML between ``---`` fences)::

    ---
    name: "example"
    stability: "stable"
    ---

Only ``experimental``, ``stable`` and ``deprecated`` are valid values.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Dict, List, Union

# Allowed lifecycle values, in the order documented in the README.
VALID_STABILITY: tuple[str, ...] = ("experimental", "stable", "deprecated")

SKILLMD_FILENAME = "SKILL.md"


def parse_frontmatter(text: str) -> Dict[str, str]:
    """Parse simple ``key: value`` YAML frontmatter from SKILL.md text.

    Frontmatter is the block delimited by the first pair of ``---`` lines.
    Values keep their raw text; surrounding single or double quotes are
    stripped. Lines without a ``:`` separator and blank/comment lines are
    ignored.
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}

    fields: Dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or ":" not in stripped:
            continue
        key, _, value = stripped.partition(":")
        key = key.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
            value = value[1:-1]
        fields[key] = value
    return fields


def read_stability(skill_md_path: Union[str, Path]) -> Union[str, None]:
    """Return the ``stability`` value from a SKILL.md file, or ``None``."""
    text = Path(skill_md_path).read_text(encoding="utf-8")
    return parse_frontmatter(text).get("stability")


def validate_stability(skill_md_path: Union[str, Path]) -> List[str]:
    """Return a list of human-readable validation errors for one SKILL.md.

    An empty list means the file declares a valid stability value. Missing
    files and missing/invalid fields are reported as errors.
    """
    path = Path(skill_md_path)
    if not path.is_file():
        return [f"{path}: file not found"]

    value = read_stability(path)
    if value is None:
        return [f"{path}: missing required 'stability' frontmatter field"]
    if value not in VALID_STABILITY:
        return [
            f"{path}: invalid stability '{value}'; "
            f"expected one of {', '.join(VALID_STABILITY)}"
        ]
    return []


def validate_skill_dir(skill_dir: Union[str, Path]) -> List[str]:
    """Validate the SKILL.md inside a skill directory."""
    return validate_stability(Path(skill_dir) / SKILLMD_FILENAME)


def main(argv: Union[List[str], None] = None) -> int:
    """CLI: validate one or more SKILL.md files or skill directories."""
    parser = argparse.ArgumentParser(
        description="Validate skill stability frontmatter.",
    )
    parser.add_argument(
        "paths",
        nargs="+",
        help="SKILL.md files or skill directories containing SKILL.md",
    )
    args = parser.parse_args(argv)

    errors: List[str] = []
    for raw in args.paths:
        path = Path(raw)
        target = path / SKILLMD_FILENAME if path.is_dir() else path
        errors.extend(validate_stability(target))

    for error in errors:
        print(error, file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
