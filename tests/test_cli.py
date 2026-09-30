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
        prompt_file = self.root / "out" / "scenes" / "s01" / "frame.txt"
        refs_file = self.root / "out" / "scenes" / "s01" / "frame.refs.txt"
        self.assertTrue(prompt_file.exists())
        self.assertTrue(refs_file.exists())
        self.assertEqual(prompt_file.read_text(encoding="utf-8"), out.rstrip("\n"))

    def test_refs_file_is_one_absolute_path_per_line(self):
        self.run_cli("frame", "s01")
        lines = (
            (self.root / "out" / "scenes" / "s01" / "frame.refs.txt")
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
            (self.root / "out" / "characters" / "skye" / "primary.sheet.refs.txt")
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
        self.assertTrue((self.root / "out" / "scenes" / "s01" / "poster.txt").exists())

    def test_location_view_selects_the_labelled_view(self):
        code, _, _ = self.run_cli("location", "church", "--view", "night")
        self.assertEqual(code, 0)
        refs = (
            (self.root / "out" / "locations" / "church" / "night.view.refs.txt")
            .read_text(encoding="utf-8")
            .splitlines()
        )
        self.assertTrue(any(p.endswith("church-night.png") for p in refs))

    def test_prop_writes_its_own_stem(self):
        code, _, _ = self.run_cli("prop", "key")
        self.assertEqual(code, 0)
        self.assertTrue((self.root / "out" / "props" / "key" / "prop.txt").exists())


class TestCliRefusalMessages(unittest.TestCase):
    """cli.py's own module docstring: every refusal prints a message naming the
    offending thing and returns 1 — never an uncaught traceback, and never a message
    that blames the wrong thing.
    """

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = make_project(pathlib.Path(self._tmp.name))
        self.bad_project = pathlib.Path(self._tmp.name) / "does-not-exist"

    def tearDown(self):
        self._tmp.cleanup()

    def run_cli(self, project, *args):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = main(["--project", str(project), *args])
        return code, out.getvalue(), err.getvalue()

    def test_sheet_refuses_a_bad_project_instead_of_crashing(self):
        code, _, err = self.run_cli(self.bad_project, "sheet", "skye")
        self.assertEqual(code, 1)
        self.assertIn("bible.json", err)

    def test_location_refuses_a_bad_project_instead_of_crashing(self):
        code, _, err = self.run_cli(self.bad_project, "location", "church")
        self.assertEqual(code, 1)
        self.assertIn("bible.json", err)

    def test_prop_refuses_a_bad_project_instead_of_crashing(self):
        code, _, err = self.run_cli(self.bad_project, "prop", "key")
        self.assertEqual(code, 1)
        self.assertIn("bible.json", err)

    def test_frame_with_a_bad_project_names_the_project_not_the_scene(self):
        code, _, err = self.run_cli(self.bad_project, "frame", "s01")
        self.assertEqual(code, 1)
        self.assertIn("bible.json", err)
        self.assertNotIn("unknown scene id", err)

    def test_motion_with_a_bad_project_names_the_project_not_the_scene(self):
        code, _, err = self.run_cli(self.bad_project, "motion", "s01", "--mode", "t2v")
        self.assertEqual(code, 1)
        self.assertIn("bible.json", err)
        self.assertNotIn("unknown scene id", err)

    def test_lint_with_a_bad_project_names_the_project_not_the_scene(self):
        code, _, err = self.run_cli(self.bad_project, "lint", "s01")
        self.assertEqual(code, 1)
        self.assertIn("bible.json", err)
        self.assertNotIn("unknown scene id", err)

    def test_unknown_character_id_message_is_not_doubled(self):
        code, _, err = self.run_cli(self.root, "sheet", "nosuch")
        self.assertEqual(code, 1)
        self.assertEqual(err.count("unknown character id"), 1, err)

    def test_unknown_location_id_message_is_not_doubled(self):
        code, _, err = self.run_cli(self.root, "location", "nosuch")
        self.assertEqual(code, 1)
        self.assertEqual(err.count("unknown location id"), 1, err)

    def test_unknown_prop_id_message_is_not_doubled(self):
        code, _, err = self.run_cli(self.root, "prop", "nosuch")
        self.assertEqual(code, 1)
        self.assertEqual(err.count("unknown prop id"), 1, err)

    def test_sheet_for_a_non_primary_look_with_no_primary_reference_refuses(self):
        bible = {
            "style": {
                "globalPreamble": "photoreal cinematic, 35mm",
                "banned": "text, watermark",
            },
            "characters": [
                {
                    "id": "skye",
                    "name": "Skye",
                    "canonicalDescription": "Woman, 29.",
                    "looks": [
                        {"label": "primary", "description": "charcoal wool coat"},
                        {"label": "casual", "description": "denim jacket"},
                    ],
                }
            ],
            "locations": [],
            "props": [],
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            (root / "scenes").mkdir(parents=True)
            (root / "refs").mkdir()
            (root / "bible.json").write_text(json.dumps(bible), encoding="utf-8")
            code, _, err = self.run_cli(root, "sheet", "skye", "--look", "casual")
        self.assertEqual(code, 1)
        self.assertIn("skye", err)
        self.assertIn("primary", err.lower())


class TestHandoff(unittest.TestCase):
    """--handoff replaces stdout with one paste-ready block; files are unaffected."""

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

    def test_handoff_still_writes_both_out_files(self):
        code, _, _ = self.run_cli("sheet", "skye", "--handoff")
        self.assertEqual(code, 0)
        out_dir = self.root / "out" / "characters" / "skye"
        self.assertTrue((out_dir / "primary.sheet.txt").exists())
        self.assertTrue((out_dir / "primary.sheet.refs.txt").exists())

    def test_handoff_block_exact_shape_with_references(self):
        code, out, _ = self.run_cli("sheet", "skye", "--handoff")
        self.assertEqual(code, 0)

        out_dir = self.root / "out" / "characters" / "skye"
        prompt_text = (out_dir / "primary.sheet.txt").read_text(encoding="utf-8")
        refs = (
            (out_dir / "primary.sheet.refs.txt")
            .read_text(encoding="utf-8")
            .splitlines()
        )
        self.assertTrue(refs)

        self.assertIn("=== PROMPT — paste this into your generator ===", out)
        self.assertIn(prompt_text, out)
        self.assertIn("=== ATTACH THESE IMAGES, IN THIS ORDER ===", out)
        for i, path in enumerate(refs, start=1):
            self.assertIn(f"{i}. {path}", out)
        # Nothing that looks like a prompt-file echo without the handoff headers.
        self.assertNotEqual(out.strip(), prompt_text.strip())

    def test_handoff_with_no_references_says_so_plainly_not_an_empty_heading(self):
        bible = {
            "style": {"globalPreamble": "photoreal cinematic, 35mm", "banned": ""},
            "characters": [],
            "locations": [],
            "props": [
                {
                    "id": "ghost",
                    "name": "Unphotographed Prop",
                    "canonicalDescription": "A plain grey box.",
                }
            ],
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            (root / "scenes").mkdir(parents=True)
            (root / "refs").mkdir()
            (root / "bible.json").write_text(json.dumps(bible), encoding="utf-8")

            out, err = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                code = main(["--project", str(root), "prop", "ghost", "--handoff"])

            self.assertEqual(code, 0)
            refs_file = root / "out" / "props" / "ghost" / "prop.refs.txt"
            self.assertEqual(refs_file.read_text(encoding="utf-8"), "")

            text = out.getvalue()
            self.assertIn("=== ATTACH THESE IMAGES, IN THIS ORDER ===", text)
            # Says plainly that none are needed, rather than an empty heading with
            # nothing under it.
            heading_idx = text.index("=== ATTACH THESE IMAGES, IN THIS ORDER ===")
            after_heading = text[heading_idx:].strip()
            self.assertNotEqual(
                after_heading, "=== ATTACH THESE IMAGES, IN THIS ORDER ==="
            )
            self.assertIn("none", after_heading.lower())

    def test_handoff_still_writes_warnings_to_stderr(self):
        (self.root / "refs" / "key.png").unlink()
        code, _, err = self.run_cli("prop", "key", "--handoff")
        self.assertEqual(code, 0)
        self.assertIn("missing reference file", err)


class TestStatusCommand(unittest.TestCase):
    """`shotkit status` — a read-only inventory, never a gate (exit 0 unless the
    project itself can't be loaded)."""

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

    def test_status_marks_present_reference_scene_without_output_and_writes_nothing(
        self,
    ):
        # key's reference file exists on disk (make_project wrote it); a second
        # scene with no rendered output yet.
        scene2 = dict(SCENE, id="s02")
        (self.root / "scenes" / "s02.json").write_text(
            json.dumps(scene2), encoding="utf-8"
        )

        code, out, _ = self.run_cli("status")
        self.assertEqual(code, 0)
        self.assertIn("[x] skye", out)
        self.assertIn("[x] church", out)
        self.assertIn("[x] key", out)
        self.assertIn("[ ] s02", out)
        self.assertFalse((self.root / "out").exists())

    def test_status_marks_a_missing_reference_file_and_a_rendered_scene(self):
        (self.root / "refs" / "key.png").unlink()
        self.run_cli("frame", "s01")  # populates out/ for s01

        code, out, _ = self.run_cli("status")
        self.assertEqual(code, 0)
        self.assertIn("[ ] key", out)
        self.assertIn("[x] s01", out)

    def test_status_refuses_a_bad_project_naming_bible_json(self):
        bad = pathlib.Path(self._tmp.name) / "does-not-exist"
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = main(["--project", str(bad), "status"])
        self.assertEqual(code, 1)
        self.assertIn("bible.json", err.getvalue())


class TestStylesCommand(unittest.TestCase):
    def test_styles_lists_all_six_presets_with_no_project_required(self):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            # No --project at all, and no cwd with a bible.json — styles is static.
            code = main(["styles"])
        self.assertEqual(code, 0)
        text = out.getvalue()
        from shotkit.style import STYLE_PRESETS

        for p in STYLE_PRESETS:
            self.assertIn(p.id, text)
            self.assertIn(p.name, text)


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
