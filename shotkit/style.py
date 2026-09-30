"""The shipped style presets: a project's medium, chosen once, repeated verbatim.

A preamble is one line that leads every prompt in the project. Authoring a fresh one
per scene is the single most common way a project loses its look — see the
prompt-assembly skill.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class StylePreset:
    id: str
    name: str
    global_preamble: str


STYLE_PRESETS: list[StylePreset] = [
    StylePreset(
        id="romance-drama",
        name="Romance drama (photoreal)",
        global_preamble=(
            "hyper-realistic editorial fashion photography, cinematic portrait lighting, "
            "natural soft directional light with gentle highlights and subtle shadows, "
            "shallow depth of field, fine skin texture with visible pores and natural detail, "
            "photoreal fabrics, high-resolution DSLR look, color-graded with warm natural tones "
            "and elegant beauty aesthetics, full photorealism"
        ),
    ),
    StylePreset(
        id="cinematic-35mm",
        name="Cinematic 35mm",
        global_preamble="cinematic, naturalistic lighting, shallow depth of field, 35mm film look",
    ),
    StylePreset(
        id="gouache-storybook",
        name="Hand-painted 2D gouache storybook",
        global_preamble=(
            "hand-painted 2D animation, storybook illustration, soft gouache and watercolor textures, "
            "gentle ink outlines, warm muted autumn palette, cozy European picture-book look, no photorealism"
        ),
    ),
    StylePreset(
        id="anime-cel",
        name="Anime cel",
        global_preamble=(
            "classic 2D anime cel animation, clean bold line art, flat cel shading, vibrant saturated palette, "
            "expressive eyes, painterly skies, no photorealism"
        ),
    ),
    StylePreset(
        id="pixar-3d",
        name="Pixar-style 3D",
        global_preamble=(
            "stylized 3D animated film look, soft global illumination, subsurface skin scattering, "
            "appealing rounded character forms, rich warm color grading, cinematic depth of field"
        ),
    ),
    StylePreset(
        id="comic-ink",
        name="Comic ink",
        global_preamble=(
            "inked comic book art, bold black linework, halftone shading, dramatic high-contrast lighting, "
            "limited spot-color palette, graphic-novel composition, no photorealism"
        ),
    ),
]


def find_preset(preset_id: str) -> StylePreset | None:
    """The preset with this id, or None."""
    return next((p for p in STYLE_PRESETS if p.id == preset_id), None)
