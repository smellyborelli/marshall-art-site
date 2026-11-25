#!/usr/bin/env python3
"""Guard README.md: a public file index, and nothing else.

Accepted shape:

    # <title>

    - <path> — <label>

Rules:
  * The first non-empty line is a level-1 heading.
  * Every other non-empty line is an entry: "- ", a path with no spaces, the
    em dash separator, and a label of 1 to 60 characters.
  * Every path exists; a path that ends in "/" is a directory.
  * No line carries internal detail: URL, email, hosting/DNS/provider notes,
    or a run of 7 or more digits.

The repository root is the parent of this file's directory, so the guard reads
the README of the tree it is installed in, whatever the current directory.

Usage:  python3 tools/readme_guard.py

Exit 0 and print "readme: index only" when the README is a clean index.
Exit 1 and print each offending line as "README.md:<n>: <reasons>: <text>".
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"

LABEL_MAX = 60
HEADING = re.compile(r"#\s+\S.*")
BANNED = re.compile(
    r"http|www\.|@|dns|mx|godaddy|deploy|formsubmit|token|secret", re.IGNORECASE
)
DIGITS = re.compile(r"\d{7,}")


def banned_hits(line: str) -> list[str]:
    """Return the distinct banned tokens in a line, in the order they appear."""
    hits = [m.group(0) for m in BANNED.finditer(line)]
    run = DIGITS.search(line)
    if run:
        hits.append(run.group(0))
    distinct = []
    for hit in hits:
        if hit not in distinct:
            distinct.append(hit)
    return distinct


def entry_problems(line: str) -> list[str]:
    """Check one "- <path> — <label>" entry. The "- " prefix is already known."""
    problems = []
    body = line[2:]
    if " — " not in body:
        return ['not a "- <path> — <label>" entry (missing the em dash separator)']

    path, _, label = body.partition(" — ")
    if not path:
        problems.append("path is empty")
    elif any(char.isspace() for char in path):
        problems.append(f"path has spaces: {path}")

    label = label.strip()
    if not 1 <= len(label) <= LABEL_MAX:
        problems.append(f"label must be 1-{LABEL_MAX} characters (found {len(label)})")

    if path and not any(char.isspace() for char in path):
        target = ROOT / path
        if path.endswith("/"):
            if not target.is_dir():
                if target.exists():
                    problems.append(f"not a directory: {path}")
                else:
                    problems.append(f"directory does not exist: {path}")
        elif not target.exists():
            problems.append(f"path does not exist: {path}")

    return problems


def main() -> int:
    if not README.exists():
        print(f"README.md: file not found at {README}")
        return 1

    problems: list[tuple[int, str, list[str]]] = []
    heading_seen = False

    for number, raw in enumerate(README.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line:
            continue

        reasons = [f"banned text {hit!r}" for hit in banned_hits(line)]

        if not heading_seen:
            heading_seen = True
            if not HEADING.fullmatch(line):
                reasons.append("first non-empty line must be a level-1 heading")
        elif not line.startswith("- "):
            reasons.append('not a "- <path> — <label>" entry')
        else:
            reasons.extend(entry_problems(line))

        if reasons:
            problems.append((number, line, reasons))

    if not heading_seen:
        print("README.md: empty — expected a level-1 heading")
        return 1

    if problems:
        for number, line, reasons in problems:
            print(f"README.md:{number}: {'; '.join(reasons)}: {line}")
        count = len(problems)
        print(f"readme: {count} offending line{'s' if count != 1 else ''}")
        return 1

    print("readme: index only")
    return 0


if __name__ == "__main__":
    sys.exit(main())
