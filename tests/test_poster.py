import unittest

from shotkit import poster


class TestCropBand(unittest.TestCase):
    def test_default_band_is_inside_the_frame(self):
        top, bottom = poster.crop_band()
        self.assertGreaterEqual(top, 0.0)
        self.assertLessEqual(bottom, 1.0)
        self.assertLess(top, bottom)

    def test_focus_y_moves_the_band_down(self):
        self.assertLess(poster.crop_band(0.1)[0], poster.crop_band(0.9)[0])

    def test_focus_y_is_clamped(self):
        self.assertEqual(poster.crop_band(-5.0), poster.crop_band(0.0))
        self.assertEqual(poster.crop_band(5.0), poster.crop_band(1.0))

    def test_clean_band_sits_inside_the_crop_band(self):
        top, bottom = poster.crop_band()
        clean_top, clean_bottom = poster.clean_band()
        self.assertEqual(clean_top, top)
        self.assertLess(clean_bottom, bottom)

    def test_compose_clause_names_percentages(self):
        clause = poster.compose_clause()
        self.assertIn("Composition constraint", clause)
        self.assertIn("%", clause)
