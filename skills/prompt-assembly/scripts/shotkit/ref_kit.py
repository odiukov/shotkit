"""Role-labelled character references — vocabulary, categories, prompt manifest.

Pure domain. The role of a reference image cannot be declared to the image API:
an image block is bytes plus a mime type and has no per-reference field, and
Imagen's typed referenceImages retired in August 2026. What the API does support — and Google
documents — is addressing inputs by position ("take the dress from the first
image"). So a role travels as TEXT, in a manifest that numbers each attached
image, and the reference file list written beside the prompt must stay in the same order as
the slots this manifest was built from.
"""

from __future__ import annotations

from collections.abc import Sequence

from shotkit.types import RefSlot

#: Display/serialisation order of the roles.
REF_ROLES: tuple[str, ...] = ("face", "body", "hair", "outfit", "object", "full")

#: The nano-banana models count references in two independent buckets with
#: separate per-model caps. A face/body/hair/whole-subject image is a "character consistency"
#: reference; a garment or a prop is an "object fidelity" reference — and must be
#: ASKED for as an object, or the model reads the person wearing it as the subject.
CHARACTER_ROLES: frozenset[str] = frozenset({"face", "body", "hair", "full"})
OBJECT_ROLES: frozenset[str] = frozenset({"outfit", "object"})


def norm_role(role: str) -> str:
    """Normalise a role; anything unrecognised degrades to "full".

    Degrading rather than raising is deliberate: a role typed by a client must
    never be able to fail a render, and "full" is exactly the behaviour that
    shipped before roles existed. That includes a role that isn't even a string
    (e.g. `role: 3` arriving over MCP) — it degrades the same as any other
    unrecognised value instead of raising AttributeError out of .strip().
    """
    if not isinstance(role, str):
        return "full"
    r = role.strip().lower()
    return r if r in REF_ROLES else "full"


_ORDINALS = (
    "first",
    "second",
    "third",
    "fourth",
    "fifth",
    "sixth",
    "seventh",
    "eighth",
    "ninth",
    "tenth",
    "eleventh",
)

_TAKE = {
    "face": (
        "the FACE of the subject: take its bone structure, eyes, nose, mouth, skin tone "
        "and skin texture, and NOTHING else"
    ),
    "body": "the subject's BODY build and proportions ONLY",
    "hair": "the subject's HAIRSTYLE and hair colour ONLY",
    "outfit": (
        "the GARMENT, read as a catalogue product shot: reproduce its cut, colour, "
        "fabric and details exactly, and treat whoever is wearing it as a mannequin"
    ),
    "object": "an OBJECT to reproduce with high fidelity",
    "full": "a reference photograph of the subject, for identity",
}

#: Roles whose image is a THING, photographed on or held by a person who is not the
#: subject. Their occupant is what bleeds.
_PROP_ROLES = frozenset({"outfit", "object"})

_HEADER = (
    "REFERENCE MANIFEST — the attached reference images are NOT interchangeable. Each "
    "supplies exactly what its entry names and nothing more; never blend them, and never "
    "carry a trait from an image whose entry does not name that trait."
)


def _ordinal(index: int) -> str:
    """ "the third image" for index 2; "image 42" once the words run out."""
    if index < len(_ORDINALS):
        return f"the {_ORDINALS[index]} image"
    return f"image {index + 1}"


def _face_source(face_at: str | None) -> str:
    """Where the face comes from, so an "ignore its face" is never left dangling.

    Naming no source is what lets the model invent a face and blend the references
    — the failure this whole module exists to remove.
    """
    if face_at:
        return f" — the face comes from {face_at}"
    return " — the subject's face comes from the identity description above"


def _ignore_clause(role: str, face_at: str | None) -> str:
    if role == "face":
        return "Ignore its clothing, background, pose and framing"
    if role == "body":
        return "Ignore its clothing, and ignore its face" + _face_source(face_at)
    if role == "hair":
        return "Ignore its face, body and clothing" + _face_source(face_at)
    if role == "outfit":
        return (
            "The person wearing it is NOT the subject: ignore their face, body and hair"
            + _face_source(face_at)
        )
    if role == "object":
        return "Ignore everything else in that image, including any person in it"
    return ""  # "full" reads the whole image as identity — nothing to exclude


def build_ref_manifest(slots: Sequence[RefSlot]) -> str:
    """Render the slot list as a positional manifest for the prompt.

    Ordinals are computed from THIS list, so the caller must send the adapter the
    same list in the same order — see shotkit/project.py.
    """
    if not slots:
        return ""
    roles = [norm_role(s.role) for s in slots]
    face_at: str | None = next(
        (_ordinal(i) for i, r in enumerate(roles) if r == "face"), None
    )
    lines = [_HEADER]
    for i, (slot, role) in enumerate(zip(slots, roles)):
        parts = [f"{_ordinal(i)} is {_TAKE[role]}"]
        if clause := _ignore_clause(role, face_at):
            parts.append(clause)
        if note := slot.note.strip():
            parts.append(f"specifically: {note}")
        lines.append(". ".join(parts) + ".")
    if closing := _closing_rule(roles, face_at):
        lines.append(closing)
    return "\n".join(lines)


def _closing_rule(roles: list[str], face_at: str | None) -> str:
    """Restate the no-bleed rule once for the whole sheet, or "" when nothing can bleed.

    Observed on a real render: the hero face panel took the face reference correctly
    while every full-body panel wore the FACE and the BUILD of the man photographed in
    the coat. The garment photo was the only full-length human attached, so the model
    used it as the template for the full-body panels and brought its occupant along.

    The per-entry prohibition existed and lost — one clause inside one entry, against
    nine full-body panels. Restating it for the sheet, LAST, puts recency behind it the
    way hoisting the manifest put primacy behind the manifest as a whole. Emitted only
    when a prop role is present: with identity references alone there is no occupant to
    leak, and an extra paragraph would only dilute the rest.
    """
    if not any(r in _PROP_ROLES for r in roles):
        return ""
    body_at = next((_ordinal(i) for i, r in enumerate(roles) if r == "body"), None)
    identity_at = face_at or next(
        (_ordinal(i) for i, r in enumerate(roles) if r == "full"), None
    )
    out = (
        "Across the whole sheet: the garment and object images above are PRODUCT "
        "references — whoever wears or holds them is a mannequin and contributes no "
        "face, no hair, no body build and no pose to any panel."
    )
    if identity_at:
        out += f" In every panel without exception the face is the face from {identity_at}."
    if body_at:
        out += f" And the build in every panel is the build from {body_at}."
    return out


def validate_ref_kit(
    slots: Sequence[RefSlot],
    *,
    max_character_refs: int,
    max_object_refs: int,
    max_total_refs: int | None = None,
) -> None:
    """Raise ValueError when a slot set exceeds what the target model will honour.

    Refusing beats trimming: the model drops the surplus references itself, without
    saying so, and the operator then reads a correct render of the wrong reference set
    as "the outfit slot did nothing".
    """
    roles = [norm_role(s.role) for s in slots]
    chars = sum(1 for r in roles if r in CHARACTER_ROLES)
    objs = sum(1 for r in roles if r in OBJECT_ROLES)
    if chars > max_character_refs:
        raise ValueError(
            f"too many character references: {chars} (face/body/hair/whole), "
            f"this image model honours {max_character_refs}"
        )
    if objs > max_object_refs:
        raise ValueError(
            f"too many object references: {objs} (outfit/object), "
            f"this image model honours {max_object_refs}"
        )
    if max_total_refs is not None and len(slots) > max_total_refs:
        raise ValueError(
            f"too many references: {len(slots)}, "
            f"this image model honours {max_total_refs} in total"
        )
