"""Batch assembly must produce final text even before reference images exist."""
from __future__ import annotations

import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest

from shotkit.cli import main


class TestBuild(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "film"
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(main(["init", str(self.root)]), 0)

    def build(self):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            result = main(["--project", str(self.root), "build"])
        return result, out.getvalue(), err.getvalue()

    def read(self, path):
        return (self.root / path).read_text()

    def update(self, path, edit):
        data = json.loads(self.read(path))
        edit(data)
        (self.root / path).write_text(json.dumps(data))

    def test_build_assembles_full_motion_and_all_references_without_images(self):
        code, out, err = self.build()
        self.assertEqual(code, 0, err)
        self.assertIn("Assembled 7/7 prompts", out)  # two chars, two views, prop, frame, motion
        for path in (
            "characters/hero/primary.sheet", "characters/ally/primary.sheet",
            "locations/warehouse/primary.view", "locations/warehouse/night.view",
            "props/case/prop", "scenes/s01/frame", "scenes/s01/motion",
        ):
            self.assertTrue(self.read(f"out/{path}.txt"))
            self.assertTrue((self.root / f"out/{path}.refs.txt").is_file())
        authored = json.loads(self.read("scenes/s01.json"))["motionPrompt"]
        assembled = self.read("out/scenes/s01/motion.txt")
        self.assertGreater(len(assembled), len(authored))
        self.assertIn("Character identities", assembled)
        self.assertIn("Audio:", assembled)
        report = json.loads(self.read("out/build-report.json"))
        self.assertTrue(report["sceneIssues"]["s01"])
        self.assertIn("missing reference file", json.dumps(report))
        self.assertFalse(list((self.root / "refs").glob("*.png")))

    def test_character_changes_propagate_to_sheet_identity_and_id_based_speech(self):
        def dialogue(scene):
            scene["dialogue"] = "@hero: Take it."
        self.update("scenes/s01.json", dialogue)
        self.assertEqual(self.build()[0], 0)
        before = self.read("out/scenes/s01/motion.txt")
        def recast(bible):
            bible["characters"][0]["name"] = "Rowan"
            bible["characters"][0]["canonicalDescription"] = "Adult woman with silver hair and green eyes."
        self.update("bible.json", recast)
        self.assertEqual(self.build()[0], 0)
        after = self.read("out/scenes/s01/motion.txt")
        self.assertNotEqual(before, after)
        self.assertIn("Rowan", after)
        self.assertIn("silver hair", after)
        self.assertNotIn("Alex Rivera", after)
        self.assertNotIn("@hero", after)
        self.assertIn("silver hair", self.read("out/characters/hero/primary.sheet.txt"))
        self.assertIn("Rowan", self.read("out/scenes/s01/frame.txt"))
        # Stable IDs and authored inputs are preserved by compilation.
        self.assertEqual(json.loads(self.read("scenes/s01.json"))["dialogue"], "@hero: Take it.")

    def test_repeat_build_is_deterministic_and_preserves_media_and_story(self):
        (self.root / "STORY.md").write_text("Author's story, do not rewrite.")
        media = self.root / "refs/hero-primary.png"
        media.write_bytes(b"existing image bytes")
        self.assertEqual(self.build()[0], 0)
        before = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(self.build()[0], 0)
        after = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(before, after)

    def test_invalid_scene_json_leaves_previous_outputs_untouched(self):
        self.assertEqual(self.build()[0], 0)
        previous = self.read("out/scenes/s01/motion.txt")
        (self.root / "scenes/s02.json").write_text('{"id":')
        code, out, err = self.build()
        self.assertEqual(code, 1)
        self.assertTrue(err)
        self.assertEqual(self.read("out/scenes/s01/motion.txt"), previous)

    def test_motion_only_scenes_do_not_get_empty_frame_prompts(self):
        self.update("scenes/s01.json", lambda s: s.pop("scenePrompt"))
        self.assertEqual(self.build()[0], 0)
        self.assertTrue((self.root / "out/scenes/s01/motion.txt").exists())
        self.assertFalse((self.root / "out/scenes/s01/frame.txt").exists())
