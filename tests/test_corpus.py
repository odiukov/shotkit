"""Corpus test: 49 scenes from a real 2-episode publish export, redacted.

`tests/corpus/story.json` is the structurally-real, textually-synthetic corpus
produced by `tools/redact_corpus.py` from a real Short Drama publish-manifest export
(335 labelled `@mentions`, 381 bare ones, `[shot N]` anchors in 47 of 49 scenes,
`SHOT N [0:00-0:04]` multishot structure). It is far harder on the resolver than any
synthetic fixture the rest of this suite uses. Every `@id`/`@id#label` token, every
`SHOT N [timecode]` header, every `[shot N]` anchor and its speaker label, every
`durationSec`, and the bible's ids and names survive from the real export, in place.
Everything else — synopses, shot descriptions, dialogue lines, titles, character/
location/prop descriptions — is deterministic filler with the SAME word count per
replaced run as the original, so the two lints that fire on word-count-vs-duration
arithmetic (`lint_dialogue_fit`) still fire on exactly the scenes they fired on
against the real text. See `tools/redact_corpus.py`'s module docstring for the full
rationale, which is the authoritative description of what the redaction keeps
and what it replaces.

The test bible defines only a "primary" look/view for every character and location —
same as the real project this was captured against — so every `#label` selector in
the corpus (`@apollo#ragged`, `@apex_office#skyline`, ...) is a label the bible does
NOT define, and every one of them must fall back to primary with a warning naming the
label. That count is cross-checked below against an independent count computed from
`parse_ref_mentions` directly, not against a hand-picked number.
"""

from __future__ import annotations

import json
import pathlib
import unittest

from shotkit.guards import narrator_voice_map
from shotkit.mentions import parse_ref_mentions
from shotkit.project import (
    Project,
    Scene,
    _character_from_json,
    _location_from_json,
    _prop_from_json,
    _scene_from_json,
    _style_from_json,
    lint_scene,
    ref_dicts,
    render_frame,
    render_motion,
)

CORPUS_DIR = pathlib.Path(__file__).resolve().parent / "corpus"
STORY = json.loads((CORPUS_DIR / "story.json").read_text(encoding="utf-8"))

# The real export's own scene ids are NOT unique across its two episodes (both
# episodes number scenes sc_1, sc_2, ... independently) — story.json is a flat list
# in the real export's own order, so scenes are identified by LIST POSITION, never by
# id alone. These three positions are the exact scenes (by index) that legitimately
# trip `lint_dialogue_fit` against the real word counts and real durationSec values —
# established once, directly against the real export, before redaction (see the Task
# 14 report for the reproduction). Word-for-word filler substitution never touches
# whitespace, so every word count — and therefore this set — survives redaction
# unchanged.
_EXPECTED_DIALOGUE_FIT_HITS = {13: "sc_9", 16: "sc_11", 23: "sc_9b8724bf"}


def _load_project() -> Project:
    return Project(
        root=CORPUS_DIR,
        style=_style_from_json(STORY["style"]),
        characters=[_character_from_json(c) for c in STORY["characters"]],
        locations=[_location_from_json(loc) for loc in STORY["locations"]],
        props=[_prop_from_json(p) for p in STORY["props"]],
    )


def _load_scenes() -> list[Scene]:
    return [_scene_from_json(s) for s in STORY["scenes"]]


class TestCorpusShape(unittest.TestCase):
    """The counts the brief calls out as "kept exactly" from the real export."""

    def test_forty_nine_scenes_across_two_episodes(self) -> None:
        self.assertEqual(len(STORY["scenes"]), 49)
        self.assertEqual(len(STORY["episodes"]), 2)
        self.assertEqual(sum(len(ep["sceneIds"]) for ep in STORY["episodes"]), 49)

    def test_seven_characters_three_locations_two_props(self) -> None:
        self.assertEqual(len(STORY["characters"]), 7)
        self.assertEqual(len(STORY["locations"]), 3)
        self.assertEqual(len(STORY["props"]), 2)

    def test_shot_n_anchors_present_in_forty_seven_of_forty_nine_scenes(self) -> None:
        import re

        anchored = sum(
            1
            for s in STORY["scenes"]
            if re.search(r"\[shot\s+\d+\]", s.get("dialogue") or "", re.IGNORECASE)
        )
        self.assertEqual(anchored, 47)


class TestCorpusRenders(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.project = _load_project()
        cls.scenes = _load_scenes()

    def test_render_frame_and_render_motion_complete_for_every_scene(self) -> None:
        for scene in self.scenes:
            with self.subTest(scene=scene.id):
                render_frame(self.project, scene)
                render_motion(self.project, scene, mode="t2v")

    def test_no_unknown_reference_anywhere(self) -> None:
        for scene in self.scenes:
            issues = lint_scene(self.project, scene)
            unknown = [i for i in issues if "unknown reference" in i]
            with self.subTest(scene=scene.id):
                self.assertEqual(unknown, [])

    def test_no_missing_reference_image_anywhere(self) -> None:
        # Every bible entity in the corpus carries a populated primary look/view/uri,
        # so a resolved mention is never "missing" its reference image either.
        for scene in self.scenes:
            issues = lint_scene(self.project, scene)
            missing = [i for i in issues if "missing reference image" in i]
            with self.subTest(scene=scene.id):
                self.assertEqual(missing, [])

    def test_no_at_token_survives_into_any_emitted_prompt(self) -> None:
        for scene in self.scenes:
            frame = render_frame(self.project, scene)
            motion = render_motion(self.project, scene, mode="t2v")
            with self.subTest(scene=scene.id):
                self.assertNotIn("@", frame.prompt)
                self.assertNotIn("@", motion.prompt)

    def test_labelled_mentions_the_bible_does_not_define_fall_back_and_warn(
        self,
    ) -> None:
        # Independent count #1: how many (scene, id) resolutions pick a LABEL selector
        # at all, straight from parse_ref_mentions — nothing about warnings here.
        refs = ref_dicts(self.project)
        expected = 0
        for scene in self.scenes:
            for entry in parse_ref_mentions(scene.motion_prompt, refs):
                if isinstance(entry["view"], dict):
                    expected += 1

        # The test bible defines no labelled look/view anywhere, so every one of
        # those resolutions must fall back to primary AND warn, naming the label.
        self.assertGreater(expected, 0, "corpus fixture lost its labelled mentions")

        # Independent count #2: the actual fallback warnings render_motion produces,
        # via a completely different code path (_select_character_look /
        # _select_location_views), not via parse_ref_mentions at all.
        actual = 0
        for scene in self.scenes:
            render = render_motion(self.project, scene, mode="t2v")
            for w in render.warnings:
                if "no look labelled" in w or "no view labelled" in w:
                    actual += 1
                    self.assertIn(
                        "using the primary",
                        w,
                        "fallback warning must name the fallback",
                    )
        self.assertEqual(actual, expected)

    def test_dialogue_fit_lint_fires_on_exactly_the_scenes_that_warrant_it(
        self,
    ) -> None:
        hits = {}
        for i, scene in enumerate(self.scenes):
            issues = lint_scene(self.project, scene)
            if any("spoken dialogue" in issue for issue in issues):
                hits[i] = scene.id
        self.assertEqual(hits, _EXPECTED_DIALOGUE_FIT_HITS)

    def test_refs_txt_order_is_stable_across_two_runs(self) -> None:
        for scene in self.scenes:
            with self.subTest(scene=scene.id, render="frame"):
                first = render_frame(self.project, scene)
                second = render_frame(self.project, scene)
                self.assertEqual(first.refs, second.refs)
            with self.subTest(scene=scene.id, render="motion"):
                first = render_motion(self.project, scene, mode="t2v")
                second = render_motion(self.project, scene, mode="t2v")
                self.assertEqual(first.refs, second.refs)

    def test_narrator_voice_map_builds_without_error_over_the_whole_roster(
        self,
    ) -> None:
        # Exercises the same call render_motion makes internally
        # (project._project_narrator_voices), directly, over every character in a
        # 7-character roster — the shape a bare `narrator_voice_map` call needs to
        # survive at corpus scale.
        voices = narrator_voice_map(
            [
                {"name": c.name, "gender": c.gender, "voiceNote": c.voice_note}
                for c in self.project.characters
            ]
        )
        self.assertEqual(len(voices), len(self.project.characters))
