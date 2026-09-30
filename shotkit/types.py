"""Project entities as plain dataclasses.

The Short Drama tool models these with pydantic; shotkit ships no dependencies, so
every field the prompt builders read is mirrored here and nothing else is. Wire names
(camelCase in JSON) are translated in shotkit/project.py, not here.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Style:
    global_preamble: str = ""
    banned: str = ""
    aspect: str | None = None


@dataclass
class Look:
    label: str
    description: str = ""
    ref_image: str | None = None


@dataclass
class RefSlot:
    """One reference image plus the role it plays in a generation."""

    uri: str
    role: str = "full"
    note: str = ""


@dataclass
class Character:
    id: str
    name: str
    canonical_description: str
    body_plan: str = "humanoid"
    looks: list[Look] = field(default_factory=list)
    identity_refs: list[str] = field(default_factory=list)
    ref_kit: list[RefSlot] = field(default_factory=list)
    reference_images: list[str] = field(default_factory=list)
    # Wire names `gender` / `voiceNote` (see project.py). Read only by the motion
    # path's narrator-voice map (guards.narrator_voice_map) — a `VO:` segment's
    # baked voice is the video model's own choice unless named, and naming it is a
    # nudge ("so the engine stops flipping the narrator's voice"), never a lock.
    gender: str = ""
    voice_note: str = ""


@dataclass
class LocationView:
    label: str
    uri: str


@dataclass
class Location:
    id: str
    name: str
    canonical_description: str
    lighting_profile: str = ""
    views: list[LocationView] = field(default_factory=list)


@dataclass
class Prop:
    id: str
    name: str
    canonical_description: str
    uri: str | None = None


_BODY_PLANS = ("humanoid", "quadruped", "wingedQuadruped", "avian")


def norm_label(label: str) -> str:
    """Normalise a look label. Not a string, or blank, means no label."""
    if not isinstance(label, str):
        return ""
    return label.strip().lower()


def norm_body_plan(value: str | None) -> str:
    """Normalise a body plan; anything unrecognised degrades to "humanoid".

    Degrading rather than raising is deliberate: a plan typed by a client must never
    be able to fail a render, and humanoid is the behaviour that shipped before body
    plans existed.
    """
    if not isinstance(value, str):
        return "humanoid"
    v = value.strip()
    return v if v in _BODY_PLANS else "humanoid"
