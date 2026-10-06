"""Exercise installed payloads without the source checkout or agent host variables."""
from __future__ import annotations

import os
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent
NAMES = {
    "cinematic-scenes", "pov-scenes", "short-drama-structure",
    "character-refs", "prompt-assembly", "scene-from-scratch",
}


class TestInstallation(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="shotkit install test ")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.project = self.base / "film workspace"
        self.project.mkdir()
        self.environment = dict(os.environ)
        for key in ("CLAUDE_PLUGIN_ROOT", "PYTHONPATH"):
            self.environment.pop(key, None)
        self.environment["PYTHONDONTWRITEBYTECODE"] = "1"

    def command(self, script, *args):
        return subprocess.run(
            [sys.executable, str(script), *map(str, args)],
            cwd=self.base, env=self.environment, text=True, capture_output=True,
        )

    def install(self):
        result = self.command(ROOT / "install.py", self.project)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result

    def snapshot(self):
        return {
            str(p.relative_to(self.project)): (
                ("link", os.readlink(p)) if p.is_symlink() else ("file", p.read_bytes())
            ) for p in self.project.rglob("*") if p.is_symlink() or p.is_file()
        }

    def test_shared_payload_survives_source_removal_and_project_move(self):
        source = self.base / "temporary source"
        source.mkdir()
        shutil.copy2(ROOT / "install.py", source / "install.py")
        shutil.copytree(ROOT / "skills", source / "skills",
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        result = self.command(source / "install.py", self.project)
        self.assertEqual(result.returncode, 0, result.stderr)
        shutil.rmtree(source)
        moved = self.base / "relocated workspace"
        self.project.rename(moved)
        self.project = moved
        canonical = moved / ".agents/skills"
        self.assertEqual({p.name for p in canonical.iterdir()}, NAMES)
        self.assertFalse((moved / ".shotkit").exists())
        for name in NAMES:
            link = moved / ".claude/skills" / name
            self.assertTrue(link.is_symlink())
            self.assertFalse(Path(os.readlink(link)).is_absolute())
            self.assertEqual(link.resolve(), (canonical / name).resolve())
        for forbidden in ("README.md", "install.py", ".claude-plugin", "tests"):
            self.assertFalse(any(p.name == forbidden for p in canonical.rglob("*")))
        cli = canonical / "prompt-assembly/scripts/shotkit.py"
        film = moved / "sample film"
        for args in (("--help",), ("init", film),
                     ("--project", film, "sheet", "hero", "--handoff")):
            result = self.command(cli, *args)
            self.assertEqual(result.returncode, 0, result.stderr)
        out = film / "out/characters/hero"
        self.assertTrue((out / "primary.sheet.txt").read_text())
        self.assertTrue((out / "primary.sheet.refs.txt").is_file())
        claude_cli = moved / ".claude/skills/prompt-assembly/scripts/shotkit.py"
        result = self.command(claude_cli, "--project", film, "status")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("hero", result.stdout)
        # Both agents must rebuild edited source JSON after the original checkout
        # is gone and the installed project has moved, without root aliases.
        scene_path = film / "scenes/s01.json"
        for entrypoint, motion in (
            (cli, "The camera slowly pans left."),
            (claude_cli, "The camera slowly pans right."),
        ):
            scene = json.loads(scene_path.read_text())
            scene["motionPrompt"] = motion
            scene_path.write_text(json.dumps(scene))
            result = self.command(entrypoint, "--project", film, "build")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Assembled 7/7 prompts", result.stdout)
            self.assertIn(motion, (film / "out/scenes/s01/motion.txt").read_text())
            report = json.loads((film / "out/build-report.json").read_text())
            for artifact in report["artifacts"]:
                self.assertTrue(artifact["assembled"], artifact)
                self.assertTrue((film / artifact["prompt"]).is_file())
                self.assertTrue((film / artifact["refs"]).is_file())

    def test_repeat_preserves_files_and_repairs_a_missing_link(self):
        self.install()
        before = self.snapshot()
        result = self.install()
        self.assertIn("0 installed, 6 unchanged", result.stdout)
        self.assertEqual(self.snapshot(), before)
        (self.project / ".claude/skills/character-refs").unlink()
        self.install()
        self.assertEqual(self.snapshot(), before)

    def test_local_edits_stop_install_before_other_missing_skills_are_restored(self):
        self.install()
        skill = self.project / ".agents/skills/scene-from-scratch/SKILL.md"
        skill.write_text(skill.read_text() + "\nLocal instruction.\n")
        shutil.rmtree(self.project / ".agents/skills/cinematic-scenes")
        before = self.snapshot()
        result = self.command(ROOT / "install.py", self.project)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Existing skill differs", result.stderr)
        self.assertEqual(self.snapshot(), before)

    def test_unrelated_claude_skill_is_preserved_without_partial_install(self):
        conflict = self.project / ".claude/skills/scene-from-scratch"
        conflict.mkdir(parents=True)
        (conflict / "SKILL.md").write_text("unrelated skill")
        before = self.snapshot()
        result = self.command(ROOT / "install.py", self.project)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.snapshot(), before)
        self.assertFalse((self.project / ".agents").exists())

    def test_redirected_parent_is_refused(self):
        outside = self.base / "outside"
        outside.mkdir()
        (self.project / ".agents").symlink_to(outside, target_is_directory=True)
        result = self.command(ROOT / "install.py", self.project)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(list(outside.iterdir()), [])

    def test_runtime_caches_are_not_installed_or_treated_as_local_edits(self):
        self.install()
        self.assertFalse(list((self.project / ".agents/skills").rglob("__pycache__")))
        cache = self.project / ".agents/skills/prompt-assembly/scripts/shotkit/__pycache__"
        cache.mkdir()
        (cache / "cli.pyc").write_bytes(b"local cache")
        self.install()
        self.assertEqual((cache / "cli.pyc").read_bytes(), b"local cache")
