import json
import pathlib
import tempfile
import unittest

from shotkit.project import (
    load_project,
    load_scene,
    lint_scene,
    ref_dicts,
    render_frame,
    render_motion,
    render_sheet,
)

BIBLE = {
    "style": {
        "globalPreamble": "photoreal cinematic, 35mm",
        "banned": "text, watermark",
    },
    "characters": [
        {
            "id": "skye",
            "name": "Skye",
            "canonicalDescription": "Woman, 29, dark eyes, black hair to the jaw.",
            "bodyPlan": "humanoid",
            "looks": [
                {
                    "label": "primary",
                    "description": "charcoal wool coat",
                    "refImage": "refs/skye-primary.png",
                }
            ],
            "refKit": [
                {"role": "face", "uri": "refs/skye-face.png", "note": "neutral"},
                {"role": "body", "uri": "refs/skye-body.png", "note": ""},
                {"role": "outfit", "uri": "refs/coat.png", "note": "no scarf"},
            ],
        }
    ],
    "locations": [
        {
            "id": "church",
            "name": "Church",
            "canonicalDescription": "A cold stone chapel, empty pews.",
            "lightingProfile": "Grey overcast daylight.",
            "views": [
                {"label": "primary", "uri": "refs/church-01.png"},
                {"label": "night", "uri": "refs/church-night.png"},
            ],
        }
    ],
    "props": [
        {
            "id": "key",
            "name": "Red Key",
            "canonicalDescription": "Brass key, red bow.",
            "uri": "refs/key.png",
        }
    ],
}

SCENE = {
    "id": "s01",
    "locationId": "church",
    "scenePrompt": "@skye kneels before the altar in @church",
    "motionPrompt": "She lifts her head toward the window",
    # 15 words ~= 7.5s at 2 words/sec, inside an 8s clip: long enough that
    # lint_dialogue_fit's "fills under half the clip" warning does not fire, short
    # enough that its overrun warning does not either. TestLints asserts a clean scene.
    "dialogue": "Skye: I never asked for any of this, and you knew it from the start.",
    "voiceover": "",
    "durationSec": 8,
    "generateAudio": True,
    "aspect": "9:16",
    "loop": False,
    "banned": "",
}


def make_project(tmp: pathlib.Path, bible=None, scene=None) -> pathlib.Path:
    (tmp / "scenes").mkdir(parents=True)
    (tmp / "refs").mkdir()
    (tmp / "bible.json").write_text(json.dumps(bible or BIBLE), encoding="utf-8")
    (tmp / "scenes" / "s01.json").write_text(
        json.dumps(scene or SCENE), encoding="utf-8"
    )
    for name in (
        "skye-primary.png",
        "skye-face.png",
        "skye-body.png",
        "coat.png",
        "church-01.png",
        "church-night.png",
        "key.png",
    ):
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
        self.assertEqual(
            self.project.style.global_preamble, "photoreal cinematic, 35mm"
        )
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
            [
                str(self.root / "refs" / n)
                for n in ("skye-face.png", "skye-body.png", "coat.png")
            ],
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


NO_REF_KIT_BIBLE = {
    "style": {
        "globalPreamble": "photoreal cinematic, 35mm",
        "banned": "text, watermark",
    },
    "characters": [
        {
            "id": "skye",
            "name": "Skye",
            "canonicalDescription": "Woman, 29, dark eyes, black hair to the jaw.",
            "identityRefs": ["refs/skye-photo1.png", "refs/skye-photo2.png"],
            "looks": [
                {
                    "label": "primary",
                    "description": "charcoal wool coat",
                    "refImage": "refs/skye-primary.png",
                }
            ],
        },
        {
            "id": "shade",
            "name": "Shade",
            "canonicalDescription": "@skye's twin, but with silver hair instead of black.",
        },
    ],
    "locations": [],
    "props": [],
}


class TestSheetNoManifestRefs(unittest.TestCase):
    """render_sheet with no refKit (no manifest): the prompt still claims identity
    photos / a base's face are attached (has_identity_photos, bases -> _identity_anchor)
    — refs must actually carry those images, matching the tool's ensure_references.py
    (identity + base-conditioning references), not ship empty beside that claim.
    """

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self._tmp.name)
        (self.root / "scenes").mkdir(parents=True)
        (self.root / "refs").mkdir()
        (self.root / "bible.json").write_text(
            json.dumps(NO_REF_KIT_BIBLE), encoding="utf-8"
        )
        for name in ("skye-primary.png", "skye-photo1.png", "skye-photo2.png"):
            (self.root / "refs" / name).write_bytes(b"\x89PNG")
        self.project = load_project(self.root)

    def tearDown(self):
        self._tmp.cleanup()

    def test_identity_photos_asserted_in_the_prompt_are_attached(self):
        r = render_sheet(self.project, "skye")
        self.assertIn("real photographs of this person", r.prompt)
        self.assertEqual(
            r.refs,
            [
                str(self.root / "refs" / "skye-photo1.png"),
                str(self.root / "refs" / "skye-photo2.png"),
            ],
        )

    def test_an_identity_variants_base_face_is_asserted_and_attached(self):
        r = render_sheet(self.project, "shade")
        self.assertIn("IDENTITY ANCHOR", r.prompt)
        self.assertTrue(
            any(p.endswith("skye-primary.png") for p in r.refs),
            f"refs did not include skye's base reference image: {r.refs}",
        )


NON_PRIMARY_LOOK_BIBLE = {
    "style": {
        "globalPreamble": "photoreal cinematic, 35mm",
        "banned": "text, watermark",
    },
    "characters": [
        {
            "id": "skye",
            "name": "Skye",
            "canonicalDescription": "Woman, 29, dark eyes, black hair to the jaw.",
            "looks": [
                {
                    "label": "primary",
                    "description": "charcoal wool coat",
                    "refImage": "refs/skye-primary.png",
                },
                {
                    "label": "casual",
                    "description": "denim jacket, sneakers",
                },
            ],
        }
    ],
    "locations": [],
    "props": [],
}

NO_PRIMARY_REF_BIBLE = {
    "style": {
        "globalPreamble": "photoreal cinematic, 35mm",
        "banned": "text, watermark",
    },
    "characters": [
        {
            "id": "skye",
            "name": "Skye",
            "canonicalDescription": "Woman, 29, dark eyes, black hair to the jaw.",
            "looks": [
                {"label": "primary", "description": "charcoal wool coat"},
                {
                    "label": "casual",
                    "description": "denim jacket, sneakers",
                },
            ],
        }
    ],
    "locations": [],
    "props": [],
}


class TestSheetNonPrimaryLookAnchor(unittest.TestCase):
    """render_sheet for a non-primary look forces the IDENTITY ONLY reference clause
    (build_character_sheet's identity_only formula: `look is not None and label !=
    "primary"`) regardless of bases or identity photos — the prompt asserts a face
    reference is attached. The no-manifest branch must actually attach the
    character's OWN PRIMARY LOOK reference image for that assertion to be true,
    mirroring the tool's generate_character_look (app/application/ensure_references.py):
    a non-primary look always anchors on `primary_look(c)` (or `reference_images[0]`),
    unconditionally, and raises when neither exists.
    """

    def _make(self, bible):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = pathlib.Path(tmp.name)
        (root / "scenes").mkdir(parents=True)
        (root / "refs").mkdir()
        (root / "bible.json").write_text(json.dumps(bible), encoding="utf-8")
        (root / "refs" / "skye-primary.png").write_bytes(b"\x89PNG")
        return load_project(root), root

    def test_a_non_primary_look_attaches_the_primary_reference_as_anchor(self):
        project, root = self._make(NON_PRIMARY_LOOK_BIBLE)
        r = render_sheet(project, "skye", look="casual")
        self.assertIn("IDENTITY ONLY", r.prompt)
        self.assertEqual(r.refs, [str(root / "refs" / "skye-primary.png")])
        self.assertEqual(r.warnings, [])

    def test_no_primary_reference_refuses_instead_of_lying(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = pathlib.Path(tmp.name)
        (root / "scenes").mkdir(parents=True)
        (root / "refs").mkdir()
        (root / "bible.json").write_text(
            json.dumps(NO_PRIMARY_REF_BIBLE), encoding="utf-8"
        )
        project = load_project(root)
        with self.assertRaises(ValueError) as ctx:
            render_sheet(project, "skye", look="casual")
        self.assertIn("skye", str(ctx.exception))
        self.assertIn("primary", str(ctx.exception).lower())


NON_PRIMARY_WITH_IDENTITY_AND_BASE_BIBLE = {
    "style": {
        "globalPreamble": "photoreal cinematic, 35mm",
        "banned": "text, watermark",
    },
    "characters": [
        {
            "id": "skye",
            "name": "Skye",
            "canonicalDescription": "Woman, 29, dark eyes, black hair to the jaw. @eli's sister.",
            "identityRefs": ["refs/skye-photo1.png", "refs/skye-photo2.png"],
            "looks": [
                {
                    "label": "primary",
                    "description": "charcoal wool coat",
                    "refImage": "refs/skye-primary.png",
                },
                {
                    "label": "casual",
                    "description": "denim jacket, sneakers",
                },
            ],
        },
        {
            "id": "eli",
            "name": "Eli",
            "canonicalDescription": "Man, 34, heavy brow, close-cropped sandy hair.",
            "looks": [
                {
                    "label": "primary",
                    "description": "grey jacket",
                    "refImage": "refs/eli-primary.png",
                }
            ],
        },
    ],
    "locations": [],
    "props": [],
}


class TestSheetNonPrimaryLookDropsIdentityAndBases(unittest.TestCase):
    """The tool's generate_character_look non-primary branch (app/application/
    ensure_references.py:240-259) zeroes BOTH identity-variant `bases` and
    `identity_refs` unconditionally once label != "primary" — `bases = []` at
    :250 and `identity = _identity_refs(c) if label == "primary" else []` at
    :253. Only the primary-look anchor (`primary_look(c)` / `reference_images[0]`)
    travels. A non-primary render must therefore:
      - attach EXACTLY that one anchor image, not identity photos or a base's face
      - read as IDENTITY ONLY generic wording, never "real photographs of this
        person" (that phrasing is gated on has_identity_photos, which the tool
        forces False for any non-primary label regardless of identity_refs)
    A character with a primary refImage, identityRefs, AND a base mentioned in
    its description exercises all three misbehaviours in one render.
    """

    def _make(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = pathlib.Path(tmp.name)
        (root / "scenes").mkdir(parents=True)
        (root / "refs").mkdir()
        (root / "bible.json").write_text(
            json.dumps(NON_PRIMARY_WITH_IDENTITY_AND_BASE_BIBLE), encoding="utf-8"
        )
        for name in (
            "skye-primary.png",
            "skye-photo1.png",
            "skye-photo2.png",
            "eli-primary.png",
        ):
            (root / "refs" / name).write_bytes(b"\x89PNG")
        return load_project(root), root

    def test_refs_are_exactly_the_primary_anchor(self):
        project, root = self._make()
        r = render_sheet(project, "skye", look="casual")
        self.assertEqual(r.refs, [str(root / "refs" / "skye-primary.png")])

    def test_prompt_uses_identity_only_wording_not_real_photographs(self):
        project, _root = self._make()
        r = render_sheet(project, "skye", look="casual")
        self.assertIn("IDENTITY ONLY", r.prompt)
        self.assertNotIn("real photographs of this person", r.prompt)

    def test_prompt_carries_no_identity_anchor_clause_for_the_base(self):
        project, _root = self._make()
        r = render_sheet(project, "skye", look="casual")
        self.assertNotIn("IDENTITY ANCHOR", r.prompt)


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


class TestMotionMentionUnion(unittest.TestCase):
    """render_motion must resolve @mentions from motionPrompt + scenePrompt, not
    motionPrompt alone — matching the tool's `present` set (scene_request.py:573-582)
    and `_build_scene_ref_budget`, both unioned. The shipped template is exactly this
    shape: scenePrompt names the cast, motionPrompt is bare camera direction.
    """

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        bible = json.loads(json.dumps(BIBLE))
        bible["characters"].append(
            {
                "id": "eli",
                "name": "Eli",
                "canonicalDescription": "Man, 34, heavy brow, close-cropped hair.",
            }
        )
        scene = dict(SCENE)
        scene["scenePrompt"] = "@skye faces @eli across the nave"
        scene["motionPrompt"] = "She lifts her head toward the window"
        self.root = make_project(pathlib.Path(self._tmp.name), bible=bible, scene=scene)
        self.project = load_project(self.root)
        self.scene = load_scene(self.project, "s01")

    def tearDown(self):
        self._tmp.cleanup()

    def test_a_character_named_only_in_scene_prompt_still_attaches_its_reference(self):
        r = render_motion(self.project, self.scene, mode="t2v")
        self.assertTrue(
            any(p.endswith("skye-primary.png") for p in r.refs),
            f"refs did not include skye's reference image: {r.refs}",
        )

    def test_the_who_is_who_threshold_counts_scene_prompt_mentions_too(self):
        # Both Skye and Eli are only @mentioned in scenePrompt; motionPrompt mentions
        # neither. With the union, that's still 2 described characters, so the
        # who-is-who clause must fire.
        r = render_motion(self.project, self.scene, mode="t2v")
        self.assertIn(
            "Character identities — match each face to its reference image", r.prompt
        )

    def test_lint_clean_scene_still_has_zero_returncode_via_the_cli_contract(self):
        # Regression guard for the exact bug report: the template's motion render
        # must not silently ship with an empty refs file while lint says nothing.
        r = render_motion(self.project, self.scene, mode="t2v")
        self.assertTrue(r.refs, "motion render attached no references at all")


class TestMotionNarratorVoice(unittest.TestCase):
    """End-to-end: bible.json's `gender`/`voiceNote` -> Character -> the VO clause.

    Exercises the full wire path (_character_from_json -> render_motion ->
    _project_narrator_voices -> build_motion_prompt), which TestMotionPromptGolden
    in test_scene.py does not: that suite calls build_motion_prompt directly with
    an already-built `voices` dict.
    """

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        bible = json.loads(json.dumps(BIBLE))
        bible["characters"].append(
            {
                "id": "eli",
                "name": "Eli",
                "canonicalDescription": "Man, 34, heavy brow, close-cropped hair.",
                "gender": "male",
                "voiceNote": "gravelly, low register",
            }
        )
        scene = dict(SCENE)
        scene["motionPrompt"] = "@skye faces @eli across the nave"
        scene["dialogue"] = (
            "Skye: I never asked for this.\nEli: VO: [shot 1] She had, once."
        )
        self.root = make_project(pathlib.Path(self._tmp.name), bible=bible, scene=scene)
        self.project = load_project(self.root)
        self.scene = load_scene(self.project, "s01")

    def tearDown(self):
        self._tmp.cleanup()

    def test_gender_and_voice_note_wire_through_to_the_vo_clause(self):
        self.assertEqual(self.project.characters[1].gender, "male")
        self.assertEqual(
            self.project.characters[1].voice_note, "gravelly, low register"
        )
        r = render_motion(self.project, self.scene, mode="t2v")
        self.assertIn(
            "an off-screen male (gravelly, low register) narrator voice-over says",
            r.prompt,
        )


class TestLints(ProjectCase):
    def test_a_broken_mention_is_reported(self):
        self.scene.scene_prompt = "@nobody waits in @church"
        self.assertTrue(
            any("@nobody" in w for w in lint_scene(self.project, self.scene))
        )

    def test_music_words_are_reported(self):
        self.scene.motion_prompt = "she hums a tune"
        self.assertTrue(any("hum" in w for w in lint_scene(self.project, self.scene)))

    def test_a_clean_scene_lints_clean(self):
        self.assertEqual(lint_scene(self.project, self.scene), [])

    def test_a_character_with_only_a_ref_kit_is_reported_missing(self):
        # ref_kit feeds the character SHEET, never a scene frame. If has_image counted
        # it, lint would call the scene clean while render_frame attached no identity
        # reference for that character — a paid render of an unanchored face.
        c = self.project.characters[0]
        c.looks = []
        c.reference_images = []
        self.assertTrue(c.ref_kit, "fixture must still carry a ref kit")
        r = render_frame(self.project, self.scene)
        self.assertFalse([p for p in r.refs if "skye" in p.lower()])
        self.assertTrue(
            [w for w in lint_scene(self.project, self.scene) if "Skye" in w]
        )

    def test_a_deleted_reference_file_is_reported_by_path(self):
        # bible.json still names refs/skye-primary.png for skye's primary look — the
        # FIELD stays populated. Only the file on disk is gone. prompt_ref_issues
        # can't see this at all: it only checks whether the field is populated, never
        # whether the path it names exists. This is the case that distinguishes the
        # two checks — a populated field pointing at nothing.
        missing_path = str(self.root / "refs" / "skye-primary.png")
        (self.root / "refs" / "skye-primary.png").unlink()
        warnings = lint_scene(self.project, self.scene)
        self.assertTrue(any(missing_path in w for w in warnings), warnings)
