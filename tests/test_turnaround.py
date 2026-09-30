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
ELI = Character(
    id="eli",
    name="Eli",
    canonical_description="Man, 34, heavy brow, close-cropped sandy hair, broad shoulders.",
)
# Mirrors tools/gen_golden.py's SKYE_WITH_IDENTITY exactly (a base @mentioned in the
# description, real identity photos, a primary look with its own refImage) — used to
# pin the primary vs. non-primary branches of generate_character_look against each
# other (app/application/ensure_references.py).
SKYE_WITH_IDENTITY = Character(
    id="skye",
    name="Skye",
    canonical_description=(
        "Woman, 29, sharp cheekbones, dark brown eyes, black hair cut to the jaw, "
        "slim athletic build. @eli's sister."
    ),
    body_plan="humanoid",
    identity_refs=["refs/skye-photo1.png", "refs/skye-photo2.png"],
    looks=[
        Look(
            label="primary",
            description="charcoal wool coat over a grey shirt",
            ref_image="refs/skye-primary.png",
        ),
        Look(label="casual", description="denim jacket, sneakers"),
    ],
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

    def test_primary_look_with_identity_photos_and_a_base(self):
        # generate_character_look's PRIMARY branch: bases = the identity-variant
        # base(s) @mentioned in the description, has_identity_photos=True because
        # label == "primary" (identity = _identity_refs(c)).
        self.assertEqual(
            build_character_sheet(
                STYLE,
                SKYE_WITH_IDENTITY,
                [ELI],
                SKYE_WITH_IDENTITY.looks[0],
                has_identity_photos=True,
            ),
            golden("sheet_primary_with_identity"),
        )

    def test_non_primary_look_drops_bases_and_identity_photos(self):
        # generate_character_look's NON-PRIMARY branch: bases = [] and
        # identity = [] UNCONDITIONALLY once label != "primary" — neither the
        # identity-variant base nor this character's own identity photos
        # condition the sheet; has_identity_photos=False.
        self.assertEqual(
            build_character_sheet(
                STYLE,
                SKYE_WITH_IDENTITY,
                [],
                SKYE_WITH_IDENTITY.looks[1],
                has_identity_photos=False,
            ),
            golden("sheet_non_primary_look"),
        )


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
