#!/usr/bin/env python3
"""Check REVIEW_SPEC_HIERARCHY against AGENTS.md's hierarchy list.

Parses the bullet list under ``## Specification document hierarchy`` in
``AGENTS.md`` and the ``REVIEW_SPEC_HIERARCHY`` env value in
``.fullsend/harness/review.yaml``, then asserts set equality.

Used as the ``spec-hierarchy-sync`` local pre-commit hook (and via
``scripts/lint.py``) so a hierarchy addition that is not also added to
the review harness fails in the same change.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_AGENTS = REPO_ROOT / "AGENTS.md"
DEFAULT_REVIEW = REPO_ROOT / ".fullsend" / "harness" / "review.yaml"

_HEADING = re.compile(r"^## Specification document hierarchy\s*$")
_ANY_HEADING = re.compile(r"^#{1,6} ")
_BULLET_PATH = re.compile(
    r"^- (?:\[`([^`]+)`\]\[[^\]]+\]|`([^`]+)`)",
)
_HIERARCHY_VALUE = re.compile(
    r"^\s*REVIEW_SPEC_HIERARCHY:\s*\"([^\"]*)\"",
    re.MULTILINE,
)


def parse_agents_hierarchy(text: str) -> list[str]:
    """Return hierarchy paths from the AGENTS.md bullet list.

    Only the section headed ``## Specification document hierarchy`` is
    scanned. A later heading ends the section, so bullets in sibling
    sections are ignored. Paths may appear as `` `path` `` or as a
    markdown link `` [`path`][ref] ``.
    """
    in_section = False
    paths: list[str] = []
    for line in text.splitlines():
        if not in_section:
            if _HEADING.match(line):
                in_section = True
            continue
        if _ANY_HEADING.match(line):
            break
        match = _BULLET_PATH.match(line)
        if match:
            paths.append(match.group(1) or match.group(2))
    if not in_section:
        raise ValueError(
            "AGENTS.md has no '## Specification document hierarchy' heading"
        )
    if not paths:
        raise ValueError("AGENTS.md 'Specification document hierarchy' list is empty")
    return paths


def parse_review_hierarchy(text: str) -> list[str]:
    """Return paths from every double-quoted REVIEW_SPEC_HIERARCHY value.

    All occurrences must contain the same path set. The value is a
    comma-separated string (whitespace around commas is ignored).
    """
    matches = _HIERARCHY_VALUE.findall(text)
    if not matches:
        raise ValueError(
            "REVIEW_SPEC_HIERARCHY not found as a double-quoted string "
            "in the review harness YAML"
        )
    parsed = [_split_paths(raw) for raw in matches]
    for i, paths in enumerate(parsed):
        if not paths:
            raise ValueError(f"REVIEW_SPEC_HIERARCHY occurrence {i + 1} is empty")
    first = set(parsed[0])
    for i, paths in enumerate(parsed[1:], start=2):
        if set(paths) != first:
            raise ValueError(
                f"REVIEW_SPEC_HIERARCHY occurrence {i} disagrees with "
                "the first occurrence"
            )
    return parsed[0]


def _split_paths(raw: str) -> list[str]:
    return [part.strip() for part in raw.split(",") if part.strip()]


def format_mismatch(agents_paths: list[str], review_paths: list[str]) -> str:
    """Return a human-readable mismatch report, or empty if in sync."""
    agents_set = set(agents_paths)
    review_set = set(review_paths)
    if agents_set == review_set:
        return ""
    lines = [
        "REVIEW_SPEC_HIERARCHY is out of sync with the",
        "'Specification document hierarchy' list in AGENTS.md.",
    ]
    missing = sorted(agents_set - review_set)
    extra = sorted(review_set - agents_set)
    if missing:
        lines.append("Missing from REVIEW_SPEC_HIERARCHY:")
        lines.extend(f"  - {path}" for path in missing)
    if extra:
        lines.append("Extra in REVIEW_SPEC_HIERARCHY:")
        lines.extend(f"  - {path}" for path in extra)
    return "\n".join(lines)


def check(agents_path: Path, review_path: Path) -> int:
    """Compare the two files. Print a report on mismatch. Return 0 or 1."""
    try:
        agents_paths = parse_agents_hierarchy(agents_path.read_text(encoding="utf-8"))
        review_paths = parse_review_hierarchy(review_path.read_text(encoding="utf-8"))
    except OSError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    report = format_mismatch(agents_paths, review_paths)
    if report:
        print(report)
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--agents",
        type=Path,
        default=DEFAULT_AGENTS,
        help="path to AGENTS.md (default: repo AGENTS.md)",
    )
    parser.add_argument(
        "--review",
        type=Path,
        default=DEFAULT_REVIEW,
        help="path to review harness YAML (default: .fullsend/harness/review.yaml)",
    )
    args = parser.parse_args(argv)
    return check(args.agents, args.review)


if __name__ == "__main__":
    sys.exit(main())
