import json
import pathlib
import tempfile
import unittest

from shotkit.project import (
    load_project, load_scene, lint_scene, ref_dicts,
    render_frame, render_motion, render_sheet,
)

BIBLE = {
    "style": {"globalPreamble": "photoreal cinematic, 35mm", "banned": "text, watermark"},
    "characters": [
        {
            "id": "skye", "name": "Skye",
            "canonicalDescription": "Woman, 29, dark eyes, black hair to the jaw.",
            "bodyPlan": "humanoid",
            "looks": [{"label": "primary", "description": "charcoal wool coat",
                       "refImage": "refs/skye-primary.png"}],
            "refKit": [
                {"role": "face", "uri": "refs/skye-face.png", "note": "neutral"},
                {"role": "body", "uri": "refs/skye-body.png", "note": ""},
                {"role": "outfit", "uri": "refs/coat.png", "note": "no scarf"},
            ],
        }
    ],
    "locations": [
        {"id": "church", "name": "Church",
         "canonicalDescription": "A cold stone chapel, empty pews.",
         "lightingProfile": "Grey overcast daylight.",
         "views": [{"label": "primary", "uri": "refs/church-01.png"},
                   {"label": "night", "uri": "refs/church-night.png"}]}
    ],
    "props": [
        {"id": "key", "name": "Red Key", "canonicalDescription": "Brass key, red bow.",
         "uri": "refs/key.png"}
    ],
}

SCENE = {
    "id": "s01", "locationId": "church",
    "scenePrompt": "@skye kneels before the altar in @church",
    "motionPrompt": "She lifts her head toward the window",
    # 15 words ~= 7.5s at 2 words/sec, inside an 8s clip: long enough that
    # lint_dialogue_fit's "fills under half the clip" warning does not fire, short
    # enough that its overrun warning does not either. TestLints asserts a clean scene.
    "dialogue": "Skye: I never asked for any of this, and you knew it from the start.",
    "voiceover": "", "durationSec": 8, "generateAudio": True,
    "aspect": "9:16", "loop": False, "banned": "",
}


def make_project(tmp: pathlib.Path, bible=None, scene=None) -> pathlib.Path:
    (tmp / "scenes").mkdir(parents=True)
    (tmp / "refs").mkdir()
    (tmp / "bible.json").write_text(json.dumps(bible or BIBLE), encoding="utf-8")
    (tmp / "scenes" / "s01.json").write_text(json.dumps(scene or SCENE), encoding="utf-8")
    for name in ("skye-primary.png", "skye-face.png", "skye-body.png", "coat.png",
                 "church-01.png", "church-night.png", "key.png"):
        (tmp / "refs" / name).write_bytes(b"\x89PNG")
    return tmp


class ProjectCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = make_project(pathlib.Path(self._tmp.name))
        self.project = load_project(self.root)
        self.scene = load_scene(self.project, "s01")

    def tearDown(self):
        self._tmp.cleanup()


class TestLoading(ProjectCase):
    def test_camel_case_wire_names_map_onto_the_dataclasses(self):
        self.assertEqual(self.project.style.global_preamble, "photoreal cinematic, 35mm")
        self.assertEqual(self.project.characters[0].canonical_description[:5], "Woman")
        self.assertEqual(self.project.locations[0].lighting_profile[:4], "Grey")
        self.assertEqual(self.project.characters[0].ref_kit[2].role, "outfit")

    def test_scene_loads(self):
        self.assertEqual(self.scene.id, "s01")
        self.assertEqual(self.scene.duration_sec, 8)
        self.assertTrue(self.scene.generate_audio)

    def test_ref_dicts_cover_every_entity(self):
        ids = {r["id"] for r in ref_dicts(self.project)}
        self.assertEqual(ids, {"skye", "church", "key"})


class TestSheetReferenceOrder(ProjectCase):
    def test_refs_are_in_slot_order_and_the_ordinals_agree(self):
        r = render_sheet(self.project, "skye")
        self.assertEqual(
            r.refs,
            [str(self.root / "refs" / n) for n in ("skye-face.png", "skye-body.png", "coat.png")],
        )
        third = [ln for ln in r.prompt.splitlines() if ln.startswith("the third image")]
        self.assertEqual(len(third), 1)
        self.assertIn("GARMENT", third[0])

    def test_a_reordered_kit_reorders_both_together(self):
        c = self.project.characters[0]
        c.ref_kit = [c.ref_kit[2], c.ref_kit[0], c.ref_kit[1]]  # outfit, face, body
        r = render_sheet(self.project, "skye")
        self.assertTrue(r.refs[0].endswith("coat.png"))
        first = [ln for ln in r.prompt.splitlines() if ln.startswith("the first image")]
        self.assertIn("GARMENT", first[0])


class TestFrameRender(ProjectCase):
    def test_mentioned_entities_contribute_refs_and_no_at_tokens_survive(self):
        r = render_frame(self.project, self.scene)
        self.assertNotIn("@skye", r.prompt)
        self.assertNotIn("@church", r.prompt)
        self.assertTrue(any(p.endswith("skye-primary.png") for p in r.refs))
        self.assertTrue(any(p.endswith("church-01.png") for p in r.refs))

    def test_a_labelled_location_view_selects_that_view(self):
        self.scene.scene_prompt = "@skye kneels in @church#night"
        r = render_frame(self.project, self.scene)
        self.assertTrue(any(p.endswith("church-night.png") for p in r.refs))
        self.assertFalse(any(p.endswith("church-01.png") for p in r.refs))

    def test_an_unknown_label_falls_back_to_primary_with_a_warning(self):
        self.scene.scene_prompt = "@skye kneels in @church#dawn"
        r = render_frame(self.project, self.scene)
        self.assertTrue(any(p.endswith("church-01.png") for p in r.refs))
        self.assertTrue(any("dawn" in w for w in r.warnings))

    def test_every_ref_path_exists_on_disk(self):
        for p in render_frame(self.project, self.scene).refs:
            self.assertTrue(pathlib.Path(p).exists(), p)


class TestMotionRender(ProjectCase):
    def test_ref_anchored_puts_the_keyframe_first(self):
        kf = str(self.root / "out" / "s01.frame.png")
        r = render_motion(self.project, self.scene, mode="ref-anchored", keyframe=kf)
        self.assertEqual(r.refs[0], kf)
        self.assertIn("@Image1 is the EXACT opening frame", r.prompt)

    def test_ref_anchored_without_a_keyframe_is_refused(self):
        with self.assertRaises(ValueError):
            render_motion(self.project, self.scene, mode="ref-anchored")


class TestLints(ProjectCase):
    def test_a_broken_mention_is_reported(self):
        self.scene.scene_prompt = "@nobody waits in @church"
        self.assertTrue(any("@nobody" in w for w in lint_scene(self.project, self.scene)))

    def test_music_words_are_reported(self):
        self.scene.motion_prompt = "she hums a tune"
        self.assertTrue(any("hum" in w for w in lint_scene(self.project, self.scene)))

    def test_a_clean_scene_lints_clean(self):
        self.assertEqual(lint_scene(self.project, self.scene), [])
