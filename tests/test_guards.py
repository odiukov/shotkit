import unittest

from shotkit import guards
from tests.support import golden

DIALOGUE = "Skye: [shot 1] I never asked for this.\nEli: Nobody does.\nVO: [shot 2] She had, once."


class TestClausesMatchTheTool(unittest.TestCase):
    def test_i2v_safety(self):
        self.assertEqual(
            guards.with_i2v_safety("She turns toward the door"), golden("i2v_safety")
        )

    def test_keyframe_anchor(self):
        self.assertEqual(
            guards.with_keyframe_anchor("She turns toward the door"),
            golden("keyframe_anchor"),
        )

    def test_audio_discipline(self):
        self.assertEqual(
            guards.with_audio_discipline("She turns", True), golden("audio_on")
        )
        self.assertEqual(
            guards.with_audio_discipline("She turns", False), golden("audio_off")
        )

    def test_spoken_line(self):
        self.assertEqual(
            guards.with_spoken_line("She turns", DIALOGUE, None), golden("spoken_line")
        )

    def test_frame_safety_tail(self):
        self.assertEqual(
            guards.frame_safety_tail("text, watermark, extra fingers"),
            golden("frame_safety_banned"),
        )
        self.assertEqual(guards.frame_safety_tail(""), golden("frame_safety_plain"))

    def test_reference_layout_clause(self):
        self.assertEqual(guards.reference_layout_clause(1), golden("ref_layout_one"))
        self.assertEqual(guards.reference_layout_clause(3), golden("ref_layout_three"))

    def test_clean_identity_description(self):
        self.assertEqual(
            guards.clean_identity_description(
                "Identity only: face, hair, build. No clothing. Woman, 29, dark eyes."
            ),
            golden("clean_identity"),
        )


class TestDialogueParsing(unittest.TestCase):
    def test_segments_carry_speaker_kind_and_shot_anchor(self):
        segs = guards.parse_dialogue(DIALOGUE)
        self.assertEqual(len(segs), 3)
        self.assertEqual(segs[0]["speaker"], "Skye")
        self.assertEqual(segs[0]["kind"], "spoken")
        self.assertEqual(segs[0]["shot"], 1)
        self.assertEqual(segs[1]["speaker"], "Eli")
        self.assertEqual(segs[1]["kind"], "spoken")
        self.assertIsNone(segs[1]["shot"])
        # A bare "VO:" segment is narration, not a character named VO — the label regex
        # reads "VO" as a speaker name, and _tag_segment blanks it.
        self.assertEqual(segs[2]["kind"], "vo")
        self.assertEqual(segs[2]["speaker"], "")
        self.assertEqual(segs[2]["shot"], 2)

    def test_spoken_and_vo_partition_the_segments(self):
        self.assertEqual(len(guards.spoken_segments(DIALOGUE)), 2)
        self.assertEqual(len(guards.vo_segments(DIALOGUE)), 1)


class TestLints(unittest.TestCase):
    def test_music_words_are_reported(self):
        self.assertIn("singing", guards.lint_music_words("she is singing softly"))
        self.assertEqual(guards.lint_music_words("she walks"), [])

    def test_dialogue_fit_warns_when_the_line_overruns_the_clip(self):
        long_line = "Skye: " + " ".join(["word"] * 40)  # ~20s at 2 words/sec
        self.assertIsNotNone(guards.lint_dialogue_fit(long_line, 8))

    def test_dialogue_fit_is_silent_on_a_well_sized_line(self):
        self.assertIsNone(
            guards.lint_dialogue_fit("Skye: " + " ".join(["word"] * 14), 8)
        )

    def test_shot_anchors_must_point_at_declared_shots(self):
        motion = "2-shot sequence. SHOT 1 — wide. HARD CUT. SHOT 2 — close."
        self.assertIsNone(guards.lint_shot_anchors(DIALOGUE, motion))
        self.assertIsNotNone(guards.lint_shot_anchors(DIALOGUE, "she turns"))

    def test_vo_in_dialogue_uses_the_baked_speech_budget(self):
        self.assertIsNotNone(guards.lint_dialogue_fit("VO: " + " ".join(["word"] * 20), 8))

    def test_spoken_and_vo_share_one_budget(self):
        self.assertIsNotNone(guards.lint_dialogue_fit(
            "Skye: " + "word " * 10 + "VO: " + "word " * 10, 8
        ))
