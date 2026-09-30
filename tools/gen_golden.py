"""Generate golden prompt fixtures from the Short Drama tool.

Run ONCE, from the shortdrama repo, with its interpreter:

    cd /Users/oleksandr/orca/projects/shortdrama
    uv run python /Users/oleksandr/orca/projects/shotkit/tools/gen_golden.py

Writes /Users/oleksandr/orca/projects/shotkit/tests/golden/*.txt.
Reads the shortdrama tree and writes nothing to it.
"""

import pathlib
import sys

OUT = pathlib.Path("/Users/oleksandr/orca/projects/shotkit/tests/golden")

from app.domain.types import Character, Location, Prop, Style, Look, RefSlot
from app.domain import ref_kit, prompt_guards, turnaround
from app.application.storyboard import build_scene_frame_prompt, build_poster_prompt

STYLE = Style(
    id="default",
    globalPreamble="photoreal cinematic, soft natural light, 35mm",
    banned="text, watermark, extra fingers",
)

SKYE = Character(
    id="skye",
    name="Skye",
    canonicalDescription=(
        "Woman, 29, sharp cheekbones, dark brown eyes, black hair cut to the jaw, "
        "slim athletic build."
    ),
    bodyPlan="humanoid",
    looks=[Look(label="primary", description="charcoal wool coat over a grey shirt")],
)

ELI = Character(
    id="eli",
    name="Eli",
    canonicalDescription="Man, 34, heavy brow, close-cropped sandy hair, broad shoulders.",
)

WOLF = Character(
    id="wolf",
    name="Wolf",
    canonicalDescription="Grey timber wolf, amber eyes, thick winter coat.",
    bodyPlan="quadruped",
)

CHURCH = Location(
    id="church",
    name="Church",
    canonicalDescription="A cold stone chapel, empty pews, tall narrow windows.",
    lightingProfile="Grey overcast daylight through the windows, no warm sources.",
)

KEY = Prop(
    id="key",
    name="Red Key",
    canonicalDescription="A small brass key with a red enamel bow, scratched.",
)

SLOTS = [
    RefSlot(uri="refs/skye-face.png", role="face", note="neutral expression"),
    RefSlot(uri="refs/skye-body.png", role="body", note=""),
    RefSlot(uri="refs/coat.png", role="outfit", note="charcoal wool, no scarf"),
]

DIALOGUE = "Skye: [shot 1] I never asked for this.\nEli: Nobody does.\nVO: [shot 2] She had, once."


def w(name: str, text: str) -> None:
    (OUT / f"{name}.txt").write_text(text, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    w(
        "frame_two_chars",
        build_scene_frame_prompt(
            "Skye kneels before the altar in the Church while Eli watches from the door",
            [SKYE, ELI],
            [CHURCH],
            [KEY],
            STYLE.global_preamble,
            STYLE.banned,
            {"skye": "charcoal wool coat over a grey shirt"},
        ),
    )
    w(
        "frame_no_entities",
        build_scene_frame_prompt(
            "An empty road at dawn",
            [],
            [],
            [],
            STYLE.global_preamble,
            "",
        ),
    )
    w(
        "poster_default_focus",
        build_poster_prompt(
            "Skye alone in the Church, the Red Key in her fist",
            [SKYE],
            [CHURCH],
            [KEY],
            STYLE.global_preamble,
            STYLE.banned,
        ),
    )

    w(
        "sheet_humanoid_primary",
        turnaround.build_character_sheet(
            STYLE,
            SKYE,
            [],
            SKYE.looks[0],
        ),
    )
    w("sheet_quadruped", turnaround.build_character_sheet(STYLE, WOLF, [], None))
    w(
        "sheet_with_manifest",
        turnaround.build_character_sheet(
            STYLE,
            SKYE,
            [],
            SKYE.looks[0],
            ref_manifest=ref_kit.build_ref_manifest(SLOTS),
        ),
    )
    w("location_view", turnaround.build_location_view(STYLE, CHURCH))
    w("prop_view", turnaround.build_prop_view(STYLE, KEY))

    w("manifest_face_body_outfit", ref_kit.build_ref_manifest(SLOTS))
    w(
        "manifest_full_only",
        ref_kit.build_ref_manifest([RefSlot(uri="a.png", role="full", note="")]),
    )
    w(
        "manifest_twelve",
        ref_kit.build_ref_manifest(
            [RefSlot(uri=f"{i}.png", role="full", note="") for i in range(12)]
        ),
    )

    w("i2v_safety", prompt_guards.with_i2v_safety("She turns toward the door"))
    w(
        "keyframe_anchor",
        prompt_guards.with_keyframe_anchor("She turns toward the door"),
    )
    w("audio_on", prompt_guards.with_audio_discipline("She turns", True))
    w("audio_off", prompt_guards.with_audio_discipline("She turns", False))
    w("spoken_line", prompt_guards.with_spoken_line("She turns", DIALOGUE, None))
    w("frame_safety_banned", prompt_guards.frame_safety_tail(STYLE.banned))
    w("frame_safety_plain", prompt_guards.frame_safety_tail(""))
    w("ref_layout_one", prompt_guards.reference_layout_clause(1))
    w("ref_layout_three", prompt_guards.reference_layout_clause(3))
    w(
        "clean_identity",
        prompt_guards.clean_identity_description(
            "Identity only: face, hair, build. No clothing. Woman, 29, dark eyes."
        ),
    )

    print(f"wrote {len(list(OUT.glob('*.txt')))} fixtures to {OUT}", file=sys.stderr)


if __name__ == "__main__":
    main()
