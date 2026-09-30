"""Generate golden prompt fixtures from the Short Drama tool.

Run ONCE, from the shortdrama repo ROOT (its `app` package is not installed —
this script puts the invoking cwd on sys.path itself, so the cwd must BE that
root), with that repo's interpreter:

    cd /Users/oleksandr/orca/projects/shortdrama
    uv run python /Users/oleksandr/orca/projects/shotkit/tools/gen_golden.py

Writes /Users/oleksandr/orca/projects/shotkit/tests/golden/*.txt.
Reads the shortdrama tree and writes nothing to it.
"""

from __future__ import annotations

import os
import pathlib
import sys

OUT = pathlib.Path("/Users/oleksandr/orca/projects/shotkit/tests/golden")

# `python /abs/path/to/script.py` puts the SCRIPT's own directory on
# sys.path[0], not the invoking cwd — so `import app...` below would fail to
# resolve shortdrama's package even when run from shortdrama's repo root, since
# that root is never installed as a package. Put the cwd on sys.path explicitly
# so the documented command actually works.
sys.path.insert(0, os.getcwd())

from app.domain.types import Character, Location, Prop, Style, Look, RefSlot
from app.domain import ref_kit, prompt_guards, turnaround
from app.domain.mentions import mentioned_ref_ids, strip_mentions
from app.application.storyboard import build_scene_frame_prompt, build_poster_prompt
from app.web.handlers.scene_request import _loop_hint as _tool_loop_hint

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

# ---------------------------------------------------------------------------
# Motion-prompt assembly fixtures
# ---------------------------------------------------------------------------
# The tool assembles a motion prompt inline inside the animate-scene REQUEST
# HANDLER (app/web/handlers/scene_request.py:602-695) — there is no single
# importable "build_motion_prompt" function to call on the tool side, only a
# sequence of pure domain-function calls threaded through a FastAPI handler
# that also resolves DB-backed adapters, ref budgets and engine selection none
# of which a golden fixture has any business depending on. `_assemble_motion`
# below reproduces that sequence literally — same domain functions
# (prompt_guards.clean_identity_description/with_spoken_line/with_i2v_safety/
# with_keyframe_anchor/with_audio_discipline, mentions.mentioned_ref_ids/
# strip_mentions, and the handler's own `_loop_hint`), called in the same
# order — so the fixture still pins what the assembled STRING is, even though
# it cannot come from one tool function because the tool has none.

# Raw dicts, not Character dataclasses: chars_raw in the tool is exactly what
# `list_characters()` hands back from the store — plain camelCase dicts — and
# the who-is-who / narrator-voice-map logic below is written against that
# shape (`c.get("id")`, `c.get("canonicalDescription")`, ...), verbatim from
# scene_request.py.
MOTION_SKYE = {
    "id": "skye",
    "name": "Skye",
    "canonicalDescription": SKYE.canonical_description,
}
MOTION_ELI = {
    "id": "eli",
    "name": "Eli",
    "canonicalDescription": ELI.canonical_description,
}
# Same two characters, with `gender` (and one `voiceNote`) set — the fields
# `narrator_voice_map` reads to build the speaker -> {gender, voiceNote} map.
MOTION_SKYE_VOICED = {**MOTION_SKYE, "gender": "female"}
MOTION_ELI_VOICED = {
    **MOTION_ELI,
    "gender": "male",
    "voiceNote": "gravelly, low register",
}

# A plain on-camera line plus an anchored, BARE "VO:" segment (no name before
# it) — narrator_voice_map has nothing to key off a bare VO tag, so this
# dialogue exercises the legacy/ungendered narration path.
DIALOGUE_BARE_VO = DIALOGUE
# The VO segment is spoken BY a named character ("Eli: VO: ...") — this is
# the shape narrator_voice_map/with_spoken_line actually resolve a gender
# against (a bare "VO:" tag carries no speaker name to look up).
DIALOGUE_NAMED_VO = (
    "Skye: [shot 1] I never asked for this.\nEli: VO: [shot 2] She had, once."
)


def _assemble_motion(
    *,
    chars_raw: list[dict],
    motion_prompt: str,
    dialogue: str,
    generate_audio: bool,
    scene_prompt: str = "",
    locs_raw: list[dict] | None = None,
    props_raw: list[dict] | None = None,
    loop: bool = False,
    anchor_keyframe: bool = False,
    ref_only: bool = False,
) -> str:
    """Reproduce scene_request.py:602-695, calling the tool's own domain functions.

    `anchor_keyframe`/`ref_only` select which ONE mode clause the tool would have
    chosen (keyframe-anchor / i2v-safety / neither, for a pure t2v ref render) —
    in the real handler those two booleans fall out of ref-budget and engine
    resolution; here the caller states the mode directly, since that resolution
    is infra this fixture generator has no business reproducing.

    `scene_prompt`/`locs_raw`/`props_raw` default to nothing because none of the
    fixtures below need them, NOT because the reproduction narrows those inputs:
    `present` (scene_request.py:573-582) is resolved against `motionPrompt + " "
    + scenePrompt`, and `ref_union` (scene_request.py:569-572) is built from
    chars + locations + props together, so a fixture that DOES need a
    scenePrompt-only mention or a location/prop mention must pass them here.
    """
    ref_union = [
        {"id": e.get("id"), "name": e.get("name", "")}
        for e in [*chars_raw, *(locs_raw or []), *(props_raw or [])]
    ]
    motion_text = " ".join(filter(None, [motion_prompt or "", scene_prompt or ""]))
    present = mentioned_ref_ids(motion_text, ref_union)
    narrator_voices = prompt_guards.narrator_voice_map(chars_raw)

    # scene_request.py:606-617 — the who-is-who clause.
    mentioned_chars = [
        (
            c,
            prompt_guards.clean_identity_description(
                c.get("canonicalDescription") or ""
            ),
        )
        for c in chars_raw
        if c.get("id") in present and (c.get("canonicalDescription") or "").strip()
    ]
    mentioned_chars = [(c, desc) for c, desc in mentioned_chars if desc]
    identity_clause = ""
    if len(mentioned_chars) >= 2:
        who = " ".join(f"{c.get('name')}: {desc}" for c, desc in mentioned_chars)
        identity_clause = (
            f"Character identities — match each face to its reference image: {who} "
        )

    # scene_request.py:676-695 — identity -> motion -> loop -> spoken line ->
    # one mode clause -> audio discipline -> strip mentions. NOTE: the assembled
    # motion string itself is built from `motionPrompt` ALONE (never `motion_text`
    # / scenePrompt) — scenePrompt only ever widens WHICH characters count toward
    # the >=2 threshold above, exactly as in the tool.
    motion = identity_clause + (motion_prompt or "")
    motion = _tool_loop_hint(motion, loop)
    motion = prompt_guards.with_spoken_line(
        motion, (dialogue or "") if generate_audio else "", narrator_voices
    )
    if anchor_keyframe:
        motion = prompt_guards.with_keyframe_anchor(motion)
    elif not ref_only:
        motion = prompt_guards.with_i2v_safety(motion)
    motion = prompt_guards.with_audio_discipline(motion, generate_audio)
    return strip_mentions(motion, ref_union)


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

    # ── Motion prompt assembly (the one output never pinned before Task 15) ──
    w(
        "motion_two_chars",
        _assemble_motion(
            chars_raw=[MOTION_SKYE, MOTION_ELI],
            motion_prompt="@skye faces @eli across the nave, neither willing to speak first",
            dialogue=DIALOGUE_BARE_VO,
            generate_audio=True,
        ),
    )
    w(
        "motion_one_char",
        _assemble_motion(
            chars_raw=[MOTION_SKYE, MOTION_ELI],
            motion_prompt="@skye kneels alone before the altar",
            dialogue=DIALOGUE_BARE_VO,
            generate_audio=True,
        ),
    )
    w(
        "motion_voices",
        _assemble_motion(
            chars_raw=[MOTION_SKYE_VOICED, MOTION_ELI_VOICED],
            motion_prompt="@skye faces @eli across the nave, neither willing to speak first",
            dialogue=DIALOGUE_NAMED_VO,
            generate_audio=True,
        ),
    )
    w(
        "motion_t2v_no_audio",
        _assemble_motion(
            chars_raw=[MOTION_SKYE, MOTION_ELI],
            motion_prompt="@skye faces @eli across the nave, neither willing to speak first",
            dialogue=DIALOGUE_BARE_VO,
            generate_audio=False,
            ref_only=True,
        ),
    )
    w(
        "motion_ref_anchored",
        _assemble_motion(
            chars_raw=[MOTION_SKYE, MOTION_ELI],
            motion_prompt="@skye faces @eli across the nave, neither willing to speak first",
            dialogue=DIALOGUE_BARE_VO,
            generate_audio=True,
            anchor_keyframe=True,
            ref_only=True,
        ),
    )

    print(f"wrote {len(list(OUT.glob('*.txt')))} fixtures to {OUT}", file=sys.stderr)


if __name__ == "__main__":
    main()
