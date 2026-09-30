import unittest

from tests.support import GOLDEN, golden

EXPECTED = [
    "frame_two_chars",
    "frame_no_entities",
    "poster_default_focus",
    "sheet_humanoid_primary",
    "sheet_quadruped",
    "sheet_with_manifest",
    "location_view",
    "prop_view",
    "manifest_face_body_outfit",
    "manifest_full_only",
    "manifest_twelve",
    "i2v_safety",
    "keyframe_anchor",
    "audio_on",
    "audio_off",
    "spoken_line",
    "frame_safety_banned",
    "frame_safety_plain",
    "ref_layout_one",
    "ref_layout_three",
    "clean_identity",
]


class TestGoldenFixtures(unittest.TestCase):
    def test_every_fixture_exists_and_is_non_empty(self):
        for name in EXPECTED:
            with self.subTest(name=name):
                self.assertTrue((GOLDEN / f"{name}.txt").exists(), name)
                self.assertTrue(golden(name).strip(), f"{name} is empty")
