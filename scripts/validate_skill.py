#!/usr/bin/env python3
"""Dependency-free structural validation for the packaged Codex skill."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "image-prompt-replication"
ENTRYPOINT = SKILL / "SKILL.md"
OPENAI_YAML = SKILL / "agents" / "openai.yaml"
WORKFLOWS = SKILL / "references" / "workflows.md"
EXPECTED_NAME = "image-prompt-replication"


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def require_file(path: Path) -> str:
    if not path.is_file():
        fail(f"missing required file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def parse_frontmatter(markdown: str) -> dict[str, str]:
    match = re.match(r"\A---\n(?P<body>.*?)\n---\n", markdown, re.DOTALL)
    if not match:
        fail("SKILL.md must begin with YAML frontmatter")

    values: dict[str, str] = {}
    for raw_line in match.group("body").splitlines():
        if not raw_line.strip() or raw_line.startswith(" "):
            continue
        key, separator, value = raw_line.partition(":")
        if separator:
            values[key.strip()] = value.strip().strip('"\'')
    return values


def validate_markdown_links(markdown: str, source: Path) -> None:
    for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", markdown):
        if "://" in target or target.startswith("#"):
            continue
        clean_target = target.split("#", 1)[0]
        if clean_target and not (source.parent / clean_target).exists():
            fail(f"broken local link in {source.relative_to(ROOT)}: {target}")


def main() -> None:
    skill_md = require_file(ENTRYPOINT)
    workflows_md = require_file(WORKFLOWS)
    openai_yaml = require_file(OPENAI_YAML)

    frontmatter = parse_frontmatter(skill_md)
    if frontmatter.get("name") != EXPECTED_NAME:
        fail(f"frontmatter name must be {EXPECTED_NAME!r}")
    if not frontmatter.get("description"):
        fail("frontmatter description must not be empty")

    combined = "\n".join((skill_md, workflows_md, openai_yaml))
    if re.search(r"\bTODO\b|\[TODO", combined, re.IGNORECASE):
        fail("unfinished TODO placeholder found")

    if f"${EXPECTED_NAME}" not in openai_yaml:
        fail("agents/openai.yaml default prompt must mention the skill explicitly")
    for heading in ("## Reconstruction", "## Correction", "## Style extraction"):
        if heading not in workflows_md:
            fail(f"missing workflow section: {heading}")

    validate_markdown_links(skill_md, ENTRYPOINT)
    print("Skill validation passed.")


if __name__ == "__main__":
    main()

