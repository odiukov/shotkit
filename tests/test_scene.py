import unittest

from shotkit.scene import (
    build_motion_prompt,
    build_poster_prompt,
    build_scene_frame_prompt,
)
from shotkit.types import Character, Location, Look, Prop, Style
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
ELI = Character(
    id="eli",
    name="Eli",
    canonical_description="Man, 34, heavy brow, close-cropped sandy hair, broad shoulders.",
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
REFS = [{"id": "skye", "name": "Skye"}, {"id": "church", "name": "Church"}]


class TestFrameMatchesTheTool(unittest.TestCase):
    def test_two_characters_a_location_and_a_prop(self):
        self.assertEqual(
            build_scene_frame_prompt(
                "Skye kneels before the altar in the Church while Eli watches from the door",
                [SKYE, ELI],
                [CHURCH],
                [KEY],
                STYLE.global_preamble,
                STYLE.banned,
                {"skye": "charcoal wool coat over a grey shirt"},
            ),
            golden("frame_two_chars"),
        )

    def test_no_entities_drops_the_reference_layout_clause(self):
        self.assertEqual(
            build_scene_frame_prompt(
                "An empty road at dawn", [], [], [], STYLE.global_preamble, ""
            ),
            golden("frame_no_entities"),
        )

    def test_poster(self):
        self.assertEqual(
            build_poster_prompt(
                "Skye alone in the Church, the Red Key in her fist",
                [SKYE],
                [CHURCH],
                [KEY],
                STYLE.global_preamble,
                STYLE.banned,
            ),
            golden("poster_default_focus"),
        )


class TestMotionModes(unittest.TestCase):
    def test_i2v_gets_the_seed_discipline_clause(self):
        out = build_motion_prompt("She turns toward the door", mode="i2v", chars=[SKYE])
        self.assertIn("Animate only what is already visible in this frame", out)
        self.assertNotIn("@Image1", out)

    def test_ref_anchored_pins_reference_one_as_frame_zero(self):
        out = build_motion_prompt(
            "She turns toward the door", mode="ref-anchored", chars=[SKYE]
        )
        self.assertIn("@Image1 is the EXACT opening frame", out)
        self.assertNotIn("Animate only what is already visible in this frame", out)

    def test_pure_t2v_gets_neither(self):
        out = build_motion_prompt("She turns toward the door", mode="t2v", chars=[SKYE])
        self.assertNotIn("@Image1 is the EXACT opening frame", out)
        self.assertNotIn("Animate only what is already visible in this frame", out)

    def test_an_unknown_mode_raises(self):
        with self.assertRaises(ValueError):
            build_motion_prompt("x", mode="magic", chars=[])


class TestMotionOrdering(unittest.TestCase):
    def test_audio_discipline_is_last_and_only_when_audio_is_baked(self):
        on = build_motion_prompt("She turns", mode="t2v", chars=[], generate_audio=True)
        off = build_motion_prompt(
            "She turns", mode="t2v", chars=[], generate_audio=False
        )
        self.assertIn("No music, no score", on)
        self.assertNotIn("No music, no score", off)

    def test_mentions_are_stripped_from_what_the_model_receives(self):
        out = build_motion_prompt(
            "@skye steps into @church", mode="t2v", chars=[SKYE], refs_for_strip=REFS
        )
        self.assertNotIn("@skye", out)
        self.assertNotIn("@church", out)
        self.assertIn("Skye steps into Church", out)

    def test_dialogue_reaches_the_prompt(self):
        out = build_motion_prompt(
            "She turns",
            mode="t2v",
            chars=[SKYE],
            dialogue="Skye: I never asked for this.",
        )
        self.assertIn("I never asked for this", out)
