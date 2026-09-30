import unittest

from shotkit.types import (
    Character,
    Location,
    LocationView,
    Look,
    Prop,
    RefSlot,
    Style,
    norm_body_plan,
    norm_label,
)


class TestTypes(unittest.TestCase):
    def test_defaults_do_not_share_state(self):
        a = Character(id="a", name="A", canonical_description="x")
        b = Character(id="b", name="B", canonical_description="y")
        a.looks.append(Look(label="primary"))
        self.assertEqual(b.looks, [])

    def test_style_defaults(self):
        s = Style()
        self.assertEqual(s.global_preamble, "")
        self.assertEqual(s.banned, "")

    def test_ref_slot_defaults_to_full(self):
        self.assertEqual(RefSlot(uri="a.png").role, "full")

    def test_norm_label_lowercases_and_trims(self):
        self.assertEqual(norm_label("  Primary  "), "primary")
        self.assertEqual(norm_label(""), "")

    def test_norm_body_plan_degrades_to_humanoid(self):
        self.assertEqual(norm_body_plan("quadruped"), "quadruped")
        self.assertEqual(norm_body_plan("wingedQuadruped"), "wingedQuadruped")
        self.assertEqual(norm_body_plan("avian"), "avian")
        self.assertEqual(norm_body_plan(None), "humanoid")
        self.assertEqual(norm_body_plan("dragonish"), "humanoid")
        self.assertEqual(norm_body_plan(7), "humanoid")

    def test_location_and_prop_shape(self):
        loc = Location(
            id="c",
            name="C",
            canonical_description="d",
            views=[LocationView(label="primary", uri="refs/c.png")],
        )
        self.assertEqual(loc.views[0].uri, "refs/c.png")
        self.assertIsNone(Prop(id="k", name="K", canonical_description="d").uri)
