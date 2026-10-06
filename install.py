#!/usr/bin/env python3
"""Install the six self-contained skills into a project for Codex and Claude Code."""
from __future__ import annotations

import argparse
import shutil
import sys
import tempfile
from pathlib import Path

NAMES = (
    "cinematic-scenes", "pov-scenes", "short-drama-structure",
    "character-refs", "prompt-assembly", "scene-from-scratch",
)
SOURCE = Path(__file__).resolve().parent / "skills"
IGNORED = {"__pycache__", ".pytest_cache", ".DS_Store"}


def ignore(directory, names):
    return [name for name in names if name in IGNORED or name.endswith(".pyc")]


def files(folder):
    """Compare real payload files, ignoring runtime caches on either side."""
    result = {}
    for path in folder.rglob("*"):
        relative = path.relative_to(folder)
        if any(part in IGNORED for part in relative.parts) or path.suffix == ".pyc":
            continue
        if path.is_symlink():
            raise ValueError(f"Inspect unexpected symlink: {path}")
        if path.is_file():
            result[relative] = path.read_bytes()
    return result


def install(project):
    if not project.is_dir():
        raise ValueError(f"Target project does not exist: {project}")
    for parent in (".agents", ".agents/skills", ".claude", ".claude/skills"):
        path = project / parent
        if path.is_symlink() or (path.exists() and not path.is_dir()):
            raise ValueError(f"Inspect destination before installing: {path}")
    destination = project / ".agents/skills"
    claude = project / ".claude/skills"
    runtime = SOURCE / "prompt-assembly/scripts"
    for path in (runtime / "shotkit.py", runtime / "shotkit/cli.py",
                 runtime / "template/bible.json"):
        if not path.is_file():
            raise ValueError(f"Incomplete source skills: missing {path}")

    # Preflight every destination before copying any skill or creating any link.
    copies, links = [], []
    for name in NAMES:
        source = SOURCE / name
        if not (source / "SKILL.md").is_file():
            raise ValueError(f"Missing source skill: {name}")
        payload = files(source)
        target = destination / name
        if target.is_symlink() or (target.exists() and not target.is_dir()):
            raise ValueError(f"Inspect existing destination: {target}")
        if target.exists():
            if files(target) != payload:
                raise ValueError(
                    f"Existing skill differs: {target}. Back up and move this folder "
                    "outside skill-discovery directories before reinstalling."
                )
        else:
            copies.append(name)
        link = claude / name
        if link.is_symlink():
            if link.resolve() != target.resolve():
                raise ValueError(f"Existing Claude link points elsewhere: {link}")
        elif link.exists():
            raise ValueError(f"Existing Claude skill is not our link: {link}")
        else:
            links.append(name)

    created = []
    try:
        # Stage and test symlink support before publishing the installation.
        with tempfile.TemporaryDirectory(prefix=".shotkit-install-", dir=project) as temp:
            stage = Path(temp)
            (stage / "link-check").symlink_to(".", target_is_directory=True)
            for name in copies:
                shutil.copytree(SOURCE / name, stage / name, ignore=ignore)
            destination.mkdir(parents=True, exist_ok=True)
            claude.mkdir(parents=True, exist_ok=True)
            for name in copies:
                target = destination / name
                (stage / name).rename(target)
                created.append(target)
            for name in links:
                link = claude / name
                link.symlink_to(f"../../.agents/skills/{name}", target_is_directory=True)
                created.append(link)
    except BaseException:
        for path in reversed(created):
            if path.is_symlink():
                path.unlink()
            else:
                shutil.rmtree(path)
        raise
    print(f"Skills: {destination} ({len(copies)} installed, {len(NAMES) - len(copies)} unchanged)")
    print(f"Claude links: {claude} ({len(links)} created)")
    print(f"CLI: {destination / 'prompt-assembly/scripts/shotkit.py'}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path, help="existing target project directory")
    args = parser.parse_args()
    if sys.version_info < (3, 9):
        parser.exit(1, "shotkit requires Python 3.9 or newer\n")
    try:
        install(args.project.expanduser().resolve())
    except (OSError, ValueError) as exc:
        parser.exit(1, f"{exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
