"""Regression coverage for input ambiguity and render/lint consistency."""

import contextlib
import copy
import io
import json
import pathlib
import tempfile
import unittest
from unittest.mock import patch

from shotkit.cli import main
from shotkit.guards import parse_dialogue
from shotkit.mentions import parse_ref_mentions, strip_mentions
from shotkit.project import load_project, load_scene, render_frame, render_location, render_motion, lint_scene
from shotkit.validation import validate_bible
from tests.test_project import BIBLE, make_project


class TestInputContract(unittest.TestCase):
    def test_namespace_collisions_are_rejected_in_both_orders(self):
        for other, message in (
            ({"id": "HERO", "name": "Bob"}, "duplicate entity id"),
            ({"id": "villain", "name": "Hero"}, "ambiguous entity name"),
            ({"id": "villain", "name": "Alice"}, "ambiguous entity name"),
        ):
            for reverse in (False, True):
                entities = [{"id": "hero", "name": "Alice"}, other]
                if reverse:
                    entities.reverse()
                with self.subTest(entities=entities):
                    with self.assertRaisesRegex(ValueError, message):
                        validate_bible({"characters": entities}, "bible.json")
                    with self.assertRaisesRegex(ValueError, message):
                        parse_ref_mentions("@hero", entities)

    def test_cross_kind_collision_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "ambiguous entity name"):
            validate_bible({"characters": [{"id": "hero", "name": "Alice"}],
                            "props": [{"id": "key", "name": "Hero"}]}, "bible.json")

    def test_own_name_can_match_id_and_mentions_remain_case_insensitive(self):
        refs = [{"id": "hero", "name": "Hero"}]
        validate_bible({"characters": refs}, "bible.json")
        self.assertEqual(strip_mentions("@HERO waits", refs), "Hero waits")

    def test_names_are_required_and_must_be_english(self):
        for changes in ({"name": ""}, {"name": " Alice "}, {"name": "\u0410\u043b\u0435\u043a\u0441\u0435\u0439"},
                        {"name": "Jos\u00e9"}, {"name": "alice"}):
            with self.subTest(changes=changes):
                with self.assertRaisesRegex(ValueError, "name"):
                    validate_bible({"characters": [{"id": "hero", **changes}]}, "bible.json")
        with self.assertRaisesRegex(ValueError, "missing required field name"):
            validate_bible({"characters": [{"id": "hero"}]}, "bible.json")

    def test_accepted_character_names_can_be_parsed_as_speakers(self):
        for name in ("Alex", "Alex Rivera", "Mary-Jane O'Neil", "Anne Marie Smith"):
            validate_bible({"characters": [{"id": "hero", "name": name}]}, "bible.json")
            self.assertEqual(parse_dialogue(f"{name}: [shot 1] Take it."),
                             [{"speaker": name, "kind": "spoken", "shot": 1, "text": "Take it."}])

    def test_ids_and_labels_must_match_mention_grammar(self):
        for value in ("hero.v2", "winter coat", "hero#night", "\u0433\u0435\u0440\u043e\u0439"):
            for key in ("id", "label"):
                bible = copy.deepcopy(BIBLE)
                target = bible["characters"][0] if key == "id" else bible["characters"][0]["looks"][0]
                target[key] = value
                with self.subTest(key=key, value=value):
                    with self.assertRaisesRegex(ValueError, key):
                        validate_bible(bible, "bible.json")
        refs = [{"id": "hero_v2", "name": "Alex", "looks": [{"label": "winter-coat"}]}]
        validate_bible({"characters": refs}, "bible.json")
        self.assertEqual(parse_ref_mentions("@hero_v2#winter-coat", refs),
                         [{"id": "hero_v2", "view": {"label": "winter-coat"}}])


class TestRenderConsistency(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = make_project(pathlib.Path(temp.name))
        self.project = load_project(self.root)
        self.scene = load_scene(self.project, "s01")

    def run_cli(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = main(["--project", str(self.root), *args])
        return code, out.getvalue(), err.getvalue()

    def test_english_only_authoring_fails_before_writing_outputs(self):
        for field in ("scenePrompt", "motionPrompt", "dialogue"):
            path = self.root / "scenes/s01.json"
            original = path.read_text()
            scene = json.loads(original)
            scene[field] = "\u041f\u0440\u0438\u0432\u0435\u0442"
            path.write_text(json.dumps(scene))
            with self.subTest(field=field):
                code, _, err = self.run_cli("build")
                self.assertEqual(code, 1)
                self.assertIn(field, err)
                self.assertIn("English", err)
                self.assertFalse((self.root / "out").exists())
            path.write_text(original)

    def test_english_punctuation_and_unicode_file_paths_are_preserved(self):
        bible = copy.deepcopy(BIBLE)
        bible["characters"][0]["canonicalDescription"] = "Woman, 29 — dark eyes, curly hair."
        bible["characters"][0]["looks"][0]["refImage"] = "refs/\u0444\u043e\u0442\u043e.png"
        (self.root / "bible.json").write_text(json.dumps(bible))
        (self.root / bible["characters"][0]["looks"][0]["refImage"]).touch()
        result = render_frame(load_project(self.root), self.scene)
        self.assertIn("Woman, 29 — dark eyes", result.prompt)
        self.assertIn(str(self.root / "refs/\u0444\u043e\u0442\u043e.png"), result.refs)

    def test_lint_includes_render_selector_warnings(self):
        for text in ("@skye#winter waits", "@skye waits in @church#missing"):
            self.scene.scene_prompt = text
            warnings = render_frame(self.project, self.scene).warnings
            self.assertTrue(warnings)
            issues = lint_scene(self.project, self.scene)
            for warning in warnings:
                self.assertIn(warning, issues)
        self.scene.scene_prompt = "@skye waits"
        self.scene.motion_prompt = "@skye#winter walks"
        for warning in render_motion(self.project, self.scene, "t2v").warnings:
            self.assertIn(warning, lint_scene(self.project, self.scene))

    def test_lint_cli_rejects_unknown_selector_without_writing(self):
        path = self.root / "scenes/s01.json"
        scene = json.loads(path.read_text())
        scene["scenePrompt"] = "@skye#winter waits"
        path.write_text(json.dumps(scene))
        code, _, err = self.run_cli("lint", "s01")
        self.assertEqual(code, 1)
        self.assertIn("@skye#winter", err)
        self.assertFalse((self.root / "out").exists())

    def test_primary_location_is_independent_of_view_order(self):
        self.project.locations[0].views.reverse()
        expected = str(self.root / "refs/church-01.png")
        for view in (None, "primary", "PRIMARY"):
            self.assertEqual(render_location(self.project, "church", view).save_to, expected)
        for mention in ("@church", "@church#primary"):
            self.scene.scene_prompt = mention
            self.assertEqual(render_frame(self.project, self.scene).refs, [expected])

    def test_location_without_primary_uses_first_view(self):
        self.project.locations[0].views = self.project.locations[0].views[1:]
        expected = str(self.root / "refs/church-night.png")
        self.assertEqual(render_location(self.project, "church").save_to, expected)
        self.scene.scene_prompt = "@church"
        self.assertEqual(render_frame(self.project, self.scene).refs, [expected])

    def test_unknown_location_view_is_refused(self):
        code, _, err = self.run_cli("location", "church", "--view", "typo")
        self.assertEqual(code, 1)
        self.assertIn("unknown view", err)
        self.assertFalse((self.root / "out").exists())

    def test_build_and_individual_commands_produce_identical_artifacts(self):
        commands = [("sheet", "skye"), ("location", "church", "--view", "primary"),
                    ("location", "church", "--view", "night"), ("prop", "key"),
                    ("frame", "s01"), ("motion", "s01", "--mode", "t2v")]
        for args in commands:
            self.assertEqual(self.run_cli(*args)[0], 0)
        before = {p: p.read_bytes() for p in (self.root / "out").rglob("*.txt")}
        with patch("shotkit.project.load_project", wraps=load_project) as load:
            self.assertEqual(self.run_cli("build")[0], 0)
        self.assertEqual(load.call_count, 1)
        self.assertEqual(before, {p: p.read_bytes() for p in (self.root / "out").rglob("*.txt")})

    def test_build_records_failed_artifact_and_continues(self):
        bible = copy.deepcopy(BIBLE)
        bible["characters"][0]["looks"] = [{"label": "winter", "description": "Wool coat"}]
        bible["characters"][0]["refKit"] = []
        bible["characters"][0]["referenceImages"] = []
        (self.root / "bible.json").write_text(json.dumps(bible))
        code, _, _ = self.run_cli("build")
        self.assertEqual(code, 1)
        report = json.loads((self.root / "out/build-report.json").read_text())
        failed = [r for r in report["artifacts"] if not r["assembled"]]
        self.assertEqual(len(failed), 1)
        self.assertIn("no primary look", failed[0]["messages"][0])
        self.assertTrue((self.root / "out/scenes/s01/motion.txt").is_file())
