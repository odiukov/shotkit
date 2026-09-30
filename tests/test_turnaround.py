import unittest

from shotkit.ref_kit import build_ref_manifest
from shotkit.turnaround import (
    build_character_sheet,
    build_location_view,
    build_prop_view,
)
from shotkit.types import Character, Location, Look, Prop, RefSlot, Style
from tests.support import golden

STYLE = Style(
    global_preamble="photoreal cinematic, soft natural light, 35mm",
    banned="text, watermark, extra fingers",
)
SKYE = Character(
    id="skye",
    name="Skye",
    canonical_description=(
        "Woman, 29, sharp cheekbones, dark brown eyes, black hair cut to the jaw, "
        "slim athletic build."
    ),
    body_plan="humanoid",
    looks=[Look(label="primary", description="charcoal wool coat over a grey shirt")],
)
WOLF = Character(
    id="wolf",
    name="Wolf",
    canonical_description="Grey timber wolf, amber eyes, thick winter coat.",
    body_plan="quadruped",
)
CHURCH = Location(
    id="church",
    name="Church",
    canonical_description="A cold stone chapel, empty pews, tall narrow windows.",
    lighting_profile="Grey overcast daylight through the windows, no warm sources.",
)
KEY = Prop(
    id="key",
    name="Red Key",
    canonical_description="A small brass key with a red enamel bow, scratched.",
)
SLOTS = [
    RefSlot(uri="refs/skye-face.png", role="face", note="neutral expression"),
    RefSlot(uri="refs/skye-body.png", role="body", note=""),
    RefSlot(uri="refs/coat.png", role="outfit", note="charcoal wool, no scarf"),
]


class TestSheetsMatchTheTool(unittest.TestCase):
    def test_humanoid_primary(self):
        self.assertEqual(
            build_character_sheet(STYLE, SKYE, [], SKYE.looks[0]),
            golden("sheet_humanoid_primary"),
        )

    def test_quadruped_uses_the_animal_layout(self):
        self.assertEqual(
            build_character_sheet(STYLE, WOLF, [], None), golden("sheet_quadruped")
        )

    def test_with_manifest(self):
        self.assertEqual(
            build_character_sheet(
                STYLE,
                SKYE,
                [],
                SKYE.looks[0],
                ref_manifest=build_ref_manifest(SLOTS),
            ),
            golden("sheet_with_manifest"),
        )

    def test_location_view(self):
        self.assertEqual(build_location_view(STYLE, CHURCH), golden("location_view"))

    def test_prop_view(self):
        self.assertEqual(build_prop_view(STYLE, KEY), golden("prop_view"))


class TestManifestSuppressesTheProse(unittest.TestCase):
    def test_subject_and_look_lines_are_dropped_not_reworded(self):
        # Two sources for one trait is a coin toss: with a manifest attached, the
        # written identity and wardrobe prose must be gone entirely.
        with_manifest = build_character_sheet(
            STYLE, SKYE, [], SKYE.looks[0], ref_manifest=build_ref_manifest(SLOTS)
        )
        self.assertNotIn("Subject identity", with_manifest)
        self.assertNotIn("Look (identical in all panels)", with_manifest)

    def test_without_a_manifest_the_prose_is_present(self):
        plain = build_character_sheet(STYLE, SKYE, [], SKYE.looks[0])
        self.assertIn("Subject identity", plain)


class TestMediumLeads(unittest.TestCase):
    def test_the_style_preamble_is_the_opening_tokens(self):
        sheet = build_character_sheet(STYLE, SKYE, [], SKYE.looks[0])
        self.assertTrue(
            sheet.startswith("photoreal cinematic, soft natural light, 35mm.")
        )

    def test_the_manifest_rides_directly_behind_the_medium(self):
        sheet = build_character_sheet(
            STYLE, SKYE, [], SKYE.looks[0], ref_manifest=build_ref_manifest(SLOTS)
        )
        lines = [ln for ln in sheet.splitlines() if ln.strip()]
        self.assertIn("REFERENCE MANIFEST", lines[2])
