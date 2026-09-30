import unittest

from shotkit.ref_kit import build_ref_manifest, norm_role, validate_ref_kit
from shotkit.types import RefSlot
from tests.support import golden

SLOTS = [
    RefSlot(uri="refs/skye-face.png", role="face", note="neutral expression"),
    RefSlot(uri="refs/skye-body.png", role="body", note=""),
    RefSlot(uri="refs/coat.png", role="outfit", note="charcoal wool, no scarf"),
]


class TestManifestMatchesTheTool(unittest.TestCase):
    def test_face_body_outfit(self):
        self.assertEqual(build_ref_manifest(SLOTS), golden("manifest_face_body_outfit"))

    def test_full_only(self):
        self.assertEqual(
            build_ref_manifest([RefSlot(uri="a.png", role="full")]),
            golden("manifest_full_only"),
        )

    def test_beyond_the_ordinal_words(self):
        self.assertEqual(
            build_ref_manifest(
                [RefSlot(uri=f"{i}.png", role="full") for i in range(12)]
            ),
            golden("manifest_twelve"),
        )

    def test_no_slots_is_an_empty_manifest(self):
        self.assertEqual(build_ref_manifest([]), "")


class TestOrdinalsTrackSlotOrder(unittest.TestCase):
    def test_each_slot_gets_its_own_ordinal_in_order(self):
        text = build_ref_manifest(SLOTS)
        self.assertLess(text.index("the first image"), text.index("the second image"))
        self.assertLess(text.index("the second image"), text.index("the third image"))

    def test_the_garment_entry_names_the_slot_that_holds_the_garment(self):
        # The outfit is slot index 2, so it must be described as the THIRD image.
        text = build_ref_manifest(SLOTS)
        third = [ln for ln in text.splitlines() if ln.startswith("the third image")]
        self.assertEqual(len(third), 1)
        self.assertIn("GARMENT", third[0])


class TestRoles(unittest.TestCase):
    def test_unknown_roles_degrade_to_full(self):
        self.assertEqual(norm_role("FACE"), "face")
        self.assertEqual(norm_role("nonsense"), "full")
        self.assertEqual(norm_role(3), "full")


class TestCaps(unittest.TestCase):
    def test_too_many_character_refs_raises(self):
        slots = [RefSlot(uri=f"{i}.png", role="face") for i in range(4)]
        with self.assertRaises(ValueError):
            validate_ref_kit(slots, max_character_refs=3, max_object_refs=3)

    def test_too_many_object_refs_raises(self):
        slots = [RefSlot(uri=f"{i}.png", role="object") for i in range(4)]
        with self.assertRaises(ValueError):
            validate_ref_kit(slots, max_character_refs=3, max_object_refs=3)

    def test_total_cap_raises(self):
        slots = [RefSlot(uri=f"{i}.png", role="face") for i in range(2)]
        slots += [RefSlot(uri=f"o{i}.png", role="object") for i in range(2)]
        with self.assertRaises(ValueError):
            validate_ref_kit(
                slots, max_character_refs=9, max_object_refs=9, max_total_refs=3
            )

    def test_within_caps_is_silent(self):
        validate_ref_kit(
            SLOTS, max_character_refs=3, max_object_refs=3, max_total_refs=6
        )
