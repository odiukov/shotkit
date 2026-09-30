import unittest

from shotkit.style import STYLE_PRESETS, find_preset


class TestPresets(unittest.TestCase):
    def test_six_presets(self):
        self.assertEqual(len(STYLE_PRESETS), 6)

    def test_ids_are_unique_and_kebab_case(self):
        ids = [p.id for p in STYLE_PRESETS]
        self.assertEqual(len(ids), len(set(ids)))
        for pid in ids:
            self.assertRegex(pid, r"^[a-z0-9]+(-[a-z0-9]+)*$")

    def test_every_preset_carries_a_preamble(self):
        for p in STYLE_PRESETS:
            self.assertTrue(p.global_preamble.strip(), p.id)

    def test_find_preset(self):
        self.assertEqual(find_preset("cinematic-35mm").name, "Cinematic 35mm")
        self.assertIsNone(find_preset("nope"))

    def test_every_preset_carries_its_negatives(self):
        # A preset is a medium AND the things that medium must not drift into. Ship the
        # preamble alone and an anime project renders photoreal the moment the model
        # feels like it — the banned list is what holds the look.
        shared = "deformed hands, extra fingers, fused limbs"
        for p in STYLE_PRESETS:
            with self.subTest(preset=p.id):
                self.assertTrue(p.banned.strip(), p.id)
                self.assertIn(shared, p.banned)
                # Each preset also names the medium it must not become.
                self.assertNotEqual(p.banned.strip(), shared)
