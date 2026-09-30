"""End-to-end run through the real entrypoint, shotkit.py — plus the two whole-repo
invariants (the 3.9 floor, and no third-party imports) that the README is about to
promise a team depends on.

Note on the init/frame/motion test below: the template (`template/bible.json`,
`template/scenes/s01.json`) ships `@hero`, `@ally` and `@case` — a earlier draft of
this plan's own text named `skye`/`church`, but the template committed in Task 11
uses `hero`/`ally`/`warehouse`/`case` (see `tests/test_cli.py::TestInit`, which already
pins the fresh-template lint names). This test follows the template as committed, not
the plan's stale snippet.
"""

from __future__ import annotations

import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent


class TestEndToEnd(unittest.TestCase):
    def test_init_then_frame_then_motion_through_the_real_entrypoint(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = pathlib.Path(tmp) / "my-film"

            def run(*args):
                return subprocess.run(
                    [sys.executable, str(ROOT / "shotkit.py"), *args],
                    capture_output=True,
                    text=True,
                )

            self.assertEqual(run("init", str(project)).returncode, 0)

            # The template's bible.json ships reference filenames that do not exist
            # yet — @hero and @ally each have a primary look refImage, @case is a
            # bare prop uri, all under refs/.
            for name in ("hero-primary.png", "ally-primary.png", "case.png"):
                (project / "refs" / name).write_bytes(b"\x89PNG")

            frame = run("--project", str(project), "frame", "s01")
            self.assertEqual(frame.returncode, 0, frame.stderr)
            self.assertTrue(frame.stdout.strip())
            self.assertTrue((project / "out" / "s01.frame.txt").exists())

            refs = (
                (project / "out" / "s01.frame.refs.txt")
                .read_text(encoding="utf-8")
                .splitlines()
            )
            self.assertTrue(refs)
            for line in refs:
                self.assertTrue(pathlib.Path(line).exists(), line)

            motion = run("--project", str(project), "motion", "s01", "--mode", "t2v")
            self.assertEqual(motion.returncode, 0, motion.stderr)
            self.assertTrue((project / "out" / "s01.motion.txt").exists())

            # The template's motionPrompt ("She walks forward across the floor,
            # glancing back once") names nobody — every @mention lives in scenePrompt
            # (@hero, @case, @ally). A new user's first motion render must still
            # attach the cast, not ship an unanchored t2v clip with an empty refs
            # file (see shotkit/project.py::render_motion's mention-union comment).
            motion_refs = (
                (project / "out" / "s01.motion.refs.txt")
                .read_text(encoding="utf-8")
                .splitlines()
            )
            self.assertTrue(motion_refs, "motion refs.txt is empty")
            for line in motion_refs:
                self.assertTrue(pathlib.Path(line).exists(), line)

    def test_pep604_annotations_have_the_future_import(self):
        # The 3.9 floor is real: `X | None` and `list[str]` in an annotation are a
        # TypeError at import time on 3.9 without the future import. Enforce it where
        # it matters — a module that annotates nothing does not need the line.
        import re

        pep604 = re.compile(r"->\s*[\w\[\]. ]+\s*\||:\s*[\w\[\]. ]+\s*\|\s*\w")
        for py in list((ROOT / "shotkit").rglob("*.py")) + [ROOT / "shotkit.py"]:
            text = py.read_text(encoding="utf-8")
            if pep604.search(text):
                with self.subTest(file=py.name):
                    self.assertIn(
                        "from __future__ import annotations",
                        text,
                        f"{py.name} uses PEP 604 annotations without the future import",
                    )

    @unittest.skipUnless(
        hasattr(sys, "stdlib_module_names"), "needs 3.10+ for sys.stdlib_module_names"
    )
    def test_no_third_party_imports_anywhere(self):
        import ast

        stdlib_ok = set(sys.stdlib_module_names)
        for py in list((ROOT / "shotkit").rglob("*.py")) + [ROOT / "shotkit.py"]:
            tree = ast.parse(py.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                mods = []
                if isinstance(node, ast.Import):
                    mods = [a.name.split(".")[0] for a in node.names]
                elif (
                    isinstance(node, ast.ImportFrom) and node.level == 0 and node.module
                ):
                    mods = [node.module.split(".")[0]]
                for m in mods:
                    with self.subTest(file=py.name, module=m):
                        self.assertTrue(
                            m in stdlib_ok or m == "shotkit",
                            f"{py.name} imports third-party module {m!r}",
                        )


if __name__ == "__main__":
    unittest.main()
