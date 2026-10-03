"""Project workflow and input errors that prompt golden files cannot exercise."""

import contextlib
import copy
import io
import json
import pathlib
import tempfile
import unittest

from shotkit.cli import main, _handoff_block
from shotkit.project import (
    load_project, load_scene, render_frame, render_motion, render_poster,
    render_location, render_prop, render_sheet, lint_scene,
)
from tests.test_project import BIBLE, SCENE, make_project


class TestWorkflowRegressions(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = make_project(pathlib.Path(tmp.name))
        self.project = load_project(self.root)
        self.scene = load_scene(self.project, "s01")

    def test_location_id_supplies_setting_and_reference_without_mention(self):
        self.scene.scene_prompt = "@skye waits"
        for render in (render_frame, render_poster):
            result = render(self.project, self.scene)
            self.assertIn("Setting: Church", result.prompt)
            self.assertIn(str(self.root / "refs/church-01.png"), result.refs)
        result = render_motion(self.project, self.scene, "t2v")
        self.assertIn(str(self.root / "refs/church-01.png"), result.refs)
        (self.root / "refs/church-01.png").unlink()
        self.assertTrue(any("church-01.png" in w for w in lint_scene(self.project, self.scene)))

    def test_explicit_location_view_overrides_default_without_extra_reference(self):
        self.scene.motion_prompt = "@skye waits in @church#night"
        result = render_motion(self.project, self.scene, "t2v")
        self.assertIn(str(self.root / "refs/church-night.png"), result.refs)
        self.assertNotIn(str(self.root / "refs/church-01.png"), result.refs)

    def test_keyframe_is_project_relative_and_i2v_has_a_separate_slot(self):
        frame = self.root / "refs/opening.png"
        frame.write_bytes(b"\x89PNG")
        anchored = render_motion(self.project, self.scene, "ref-anchored", "refs/opening.png")
        self.assertEqual(anchored.refs[0], str(frame))
        self.assertEqual(anchored.warnings, [])
        i2v = render_motion(self.project, self.scene, "i2v", "refs/opening.png")
        self.assertNotIn(str(frame), i2v.refs)
        self.assertEqual(i2v.start_frame, str(frame))
        self.assertIn(str(frame), _handoff_block(i2v))
        self.assertIn("separate from reference images", _handoff_block(i2v))
        with self.assertRaisesRegex(ValueError, "t2v"):
            render_motion(self.project, self.scene, "t2v", "refs/opening.png")

    def test_missing_i2v_keyframe_is_reported(self):
        result = render_motion(self.project, self.scene, "i2v", "refs/missing.png")
        self.assertTrue(any(str(self.root / "refs/missing.png") in w for w in result.warnings))

    def test_style_and_manual_settings_reach_handoff(self):
        self.project.style.aspect = "16:9"
        result = render_motion(self.project, self.scene, "t2v")
        self.assertTrue(result.prompt.startswith(self.project.style.global_preamble + "\n"))
        handoff = _handoff_block(result)
        self.assertIn("Aspect ratio: 9:16", handoff)
        self.assertIn("Duration: 8 seconds", handoff)
        self.scene.aspect = None
        self.assertEqual(render_frame(self.project, self.scene).aspect, "16:9")
        self.assertEqual(render_motion(self.project, self.scene, "t2v").aspect, "16:9")
        self.assertEqual(render_poster(self.project, self.scene).aspect, "9:16")

    def test_first_prop_and_location_have_destinations_without_missing_inputs(self):
        for name in ("key.png", "church-01.png", "church-night.png"):
            (self.root / "refs" / name).unlink()
        for result, name in (
            (render_prop(self.project, "key"), "key.png"),
            (render_location(self.project, "church"), "church-01.png"),
            (render_location(self.project, "church", "night"), "church-night.png"),
        ):
            self.assertEqual(result.refs, [])
            self.assertEqual(result.warnings, [])
            self.assertEqual(result.save_to, str(self.root / "refs" / name))
            self.assertIn(name, _handoff_block(result))

    def test_existing_location_inputs_and_save_destination_are_both_shown(self):
        (self.root / "refs/church-night.png").unlink()
        result = render_location(self.project, "church", "night")
        self.assertEqual(result.refs, [str(self.root / "refs/church-01.png")])
        handoff = _handoff_block(result)
        self.assertIn("church-01.png", handoff)
        self.assertIn("church-night.png", handoff)

    def test_unknown_look_is_an_error_even_with_a_ref_kit(self):
        with self.assertRaisesRegex(ValueError, "unknown look.*typo"):
            render_sheet(self.project, "skye", "typo")

    def test_narration_is_generated_from_dialogue_and_counted_by_lint(self):
        self.scene.dialogue = "Skye: VO: " + "word " * 20
        result = render_motion(self.project, self.scene, "t2v")
        self.assertIn("narrator voice-over", result.prompt)
        self.assertTrue(any("longer than" in w for w in lint_scene(self.project, self.scene)))
        self.scene.generate_audio = False
        self.assertTrue(any("generateAudio" in w for w in lint_scene(self.project, self.scene)))
        self.assertNotIn("narrator voice-over", render_motion(self.project, self.scene, "t2v").prompt)

    def assert_cli_error(self, phrase):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = main(["--project", str(self.root), "frame", "s01"])
        self.assertEqual(code, 1)
        self.assertIn(phrase, err.getvalue())
        self.assertNotIn("Traceback", err.getvalue())
        self.assertFalse((self.root / "out").exists())

    def test_scene_validation_and_legacy_migration_errors_are_actionable(self):
        for changes, phrase in (
            ({"motionPromt": "lost"}, "motionPromt"),
            ({"durationSec": "8"}, "durationSec"),
            ({"durationSec": -1}, "positive"),
            ({"generateAudio": "false"}, "generateAudio"),
            ({"dialogue": None}, "dialogue"),
            ({"aspect": "wide"}, "aspect"),
            ({"voiceover": "Do not lose this narration"}, "dialogue as 'VO:"),
            ({"locationId": "missing"}, "unknown location"),
        ):
            with self.subTest(changes=changes):
                (self.root / "scenes/s01.json").write_text(json.dumps(dict(SCENE, **changes)))
                self.assert_cli_error(phrase)

    def test_bible_nested_errors_and_duplicate_ids_are_rejected(self):
        for mutation, phrase in (
            (lambda b: b["style"].update(globalPreambl="lost"), "globalPreambl"),
            (lambda b: b["characters"][0].update(looks="primary"), "looks"),
            (lambda b: b["props"][0].update(id="skye"), "duplicate entity id"),
            (lambda b: b["characters"][0].update(id="../escape"), "path separators"),
        ):
            with self.subTest(phrase=phrase):
                bible = copy.deepcopy(BIBLE)
                mutation(bible)
                (self.root / "bible.json").write_text(json.dumps(bible))
                self.assert_cli_error(phrase)

    def test_invalid_json_produces_a_cli_error_without_traceback(self):
        (self.root / "bible.json").write_text("{")
        self.assert_cli_error("Expecting property name")
