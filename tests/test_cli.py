import contextlib
import io
import json
import pathlib
import tempfile
import unittest

from shotkit.cli import main
from tests.test_project import SCENE, make_project


class TestCli(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = make_project(pathlib.Path(self._tmp.name))

    def tearDown(self):
        self._tmp.cleanup()

    def run_cli(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = main(["--project", str(self.root), *args])
        return code, out.getvalue(), err.getvalue()

    def test_frame_writes_both_files_and_echoes_the_prompt(self):
        code, out, _ = self.run_cli("frame", "s01")
        self.assertEqual(code, 0)
        prompt_file = self.root / "out" / "s01.frame.txt"
        refs_file = self.root / "out" / "s01.frame.refs.txt"
        self.assertTrue(prompt_file.exists())
        self.assertTrue(refs_file.exists())
        self.assertEqual(prompt_file.read_text(encoding="utf-8"), out.rstrip("\n"))

    def test_refs_file_is_one_absolute_path_per_line(self):
        self.run_cli("frame", "s01")
        lines = (
            (self.root / "out" / "s01.frame.refs.txt")
            .read_text(encoding="utf-8")
            .splitlines()
        )
        self.assertTrue(lines)
        for line in lines:
            self.assertTrue(pathlib.Path(line).is_absolute(), line)
            self.assertTrue(pathlib.Path(line).exists(), line)

    def test_sheet_writes_refs_in_slot_order(self):
        self.run_cli("sheet", "skye")
        lines = (
            (self.root / "out" / "skye.primary.sheet.refs.txt")
            .read_text(encoding="utf-8")
            .splitlines()
        )
        self.assertEqual(
            [pathlib.Path(p).name for p in lines],
            ["skye-face.png", "skye-body.png", "coat.png"],
        )

    def test_motion_requires_a_mode(self):
        code, _, err = self.run_cli("motion", "s01")
        self.assertEqual(code, 1)
        self.assertIn("--mode", err)

    def test_ref_anchored_without_a_keyframe_exits_one(self):
        code, _, err = self.run_cli("motion", "s01", "--mode", "ref-anchored")
        self.assertEqual(code, 1)
        self.assertIn("keyframe", err.lower())

    def test_lint_exits_one_on_a_broken_mention(self):
        scene = dict(SCENE, scenePrompt="@nobody waits in @church")
        (self.root / "scenes" / "s01.json").write_text(
            json.dumps(scene), encoding="utf-8"
        )
        code, _, err = self.run_cli("lint", "s01")
        self.assertEqual(code, 1)
        self.assertIn("@nobody", err)

    def test_lint_exits_zero_on_a_clean_scene(self):
        code, _, _ = self.run_cli("lint", "s01")
        self.assertEqual(code, 0)

    def test_unknown_scene_exits_one_with_the_id_in_the_message(self):
        code, _, err = self.run_cli("frame", "s99")
        self.assertEqual(code, 1)
        self.assertIn("s99", err)

    def test_poster_writes_its_own_stem(self):
        code, _, _ = self.run_cli("poster", "s01")
        self.assertEqual(code, 0)
        self.assertTrue((self.root / "out" / "s01.poster.txt").exists())

    def test_location_view_selects_the_labelled_view(self):
        code, _, _ = self.run_cli("location", "church", "--view", "night")
        self.assertEqual(code, 0)
        refs = (
            (self.root / "out" / "church.night.view.refs.txt")
            .read_text(encoding="utf-8")
            .splitlines()
        )
        self.assertTrue(any(p.endswith("church-night.png") for p in refs))

    def test_prop_writes_its_own_stem(self):
        code, _, _ = self.run_cli("prop", "key")
        self.assertEqual(code, 0)
        self.assertTrue((self.root / "out" / "key.prop.txt").exists())


class TestInit(unittest.TestCase):
    def test_init_copies_the_template(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = pathlib.Path(tmp) / "my-film"
            out, err = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                code = main(["init", str(target)])
            self.assertEqual(code, 0)
            self.assertTrue((target / "bible.json").exists())
            self.assertTrue((target / "scenes" / "s01.json").exists())
            self.assertTrue((target / "refs").is_dir())
            json.loads((target / "bible.json").read_text(encoding="utf-8"))

    def test_init_refuses_a_non_empty_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = pathlib.Path(tmp) / "taken"
            target.mkdir()
            (target / "keep.txt").write_text("x", encoding="utf-8")
            err = io.StringIO()
            with (
                contextlib.redirect_stdout(io.StringIO()),
                contextlib.redirect_stderr(err),
            ):
                code = main(["init", str(target)])
            self.assertEqual(code, 1)
            self.assertTrue((target / "keep.txt").exists())

    def test_freshly_initialized_template_lints_non_clean_naming_its_missing_files(
        self,
    ):
        # The template's reference filenames deliberately point at files that do not
        # exist under refs/ yet (only .gitkeep is there). This is the first lesson a
        # new user should see: lint on the fresh scaffold is NOT clean, and it names
        # exactly which files are missing.
        with tempfile.TemporaryDirectory() as tmp:
            target = pathlib.Path(tmp) / "fresh-film"
            with (
                contextlib.redirect_stdout(io.StringIO()),
                contextlib.redirect_stderr(io.StringIO()),
            ):
                init_code = main(["init", str(target)])
            self.assertEqual(init_code, 0)

            out, err = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                code = main(["--project", str(target), "lint", "s01"])
            self.assertEqual(code, 1)
            err_text = err.getvalue()
            self.assertIn("hero-primary.png", err_text)
            self.assertIn("case.png", err_text)
            self.assertIn("ally-primary.png", err_text)
