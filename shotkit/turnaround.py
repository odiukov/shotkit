"""Reference-image prompts (character sheets, location/prop hero frames) — port
of src/domain/turnaround.ts.

Pure; only domain imports. Only the Style section varies per project. The
character sheet's panel layout is fixed per BODY PLAN; location and prop views are
single unbroken frames. Identity is copied verbatim.
"""

from __future__ import annotations

from dataclasses import dataclass

from shotkit.types import (
    Character,
    Location,
    Look,
    Prop,
    Style,
    norm_body_plan,
    norm_label,
)
from shotkit.mentions import strip_mentions
from shotkit.guards import clean_identity_description


@dataclass(frozen=True)
class _PlanSpec:
    """Everything in the sheet prompt that depends on the subject's anatomy.

    Anatomy is data, not control flow: the identity scaffolding around these slots —
    the subject line, the identity anchor, the reference clause, the style block and
    the layout tail — is shared by every plan and exists in exactly one copy.
    """

    subject_noun: str  # "person" | "animal" | "creature" | "bird"
    head_noun: str  # "face" for humanoid, "head" otherwise
    identity_traits: str  # tail of "Same X in every panel — identical …"
    top: str  # top section (identity focus)
    middle: str  # middle section (full-body panels)
    lower: str  # lower section (angles / gait)
    guard: str  # anatomy negative clause; "" for humanoid, which drops the line
    detail_noun: str  # what full-body panels preserve besides proportions — "outfit detail" for humanoid
    sheet_noun: str  # what stays prioritised at the top — "face sheet" for humanoid, "head sheet" otherwise


# The humanoid spec holds LITERAL copies of the strings this file shipped before body
# plans existed, and `guard` is "" so the extra line is filtered out by the `if p`
# comprehension at the bottom of build_character_sheet. The humanoid prompt is therefore
# byte-for-byte unchanged — pinned by tests/domain/test_turnaround_golden.py.
_HUMANOID = _PlanSpec(
    subject_noun="person",
    head_noun="face",
    identity_traits="face, hair, body and outfit",
    top=(
        "Top section (identity focus): one very large hero face/head close-up spanning ~50-60% width as the main visual anchor, "
        "beside a compact head rotation grid showing the SAME head at DISTINCT angles — never repeat the frontal view: "
        "front, three-quarter left, left profile, rear / back of head, looking up, looking down — plus one supporting portrait crop. "
        "This top row must immediately establish facial identity."
    ),
    middle="Middle section: three evenly spaced full-body panels — T-pose front, T-pose back, front neutral.",
    lower=(
        "Lower section: side-left, side-right, 3/4 front, 3/4 back, full back, and a relaxed walking pose, "
        "in clean stacked rows with balanced spacing. Do NOT include any top-down / overhead view (it distorts into blobs)."
    ),
    guard="",
    detail_noun="outfit detail",
    sheet_noun="face sheet",
)

# A four-legged animal. The profile silhouette carries more identity than the frontal
# view here (the opposite of a human sheet), so both profiles get an explicit width
# instruction instead of sharing a cramped row.
_QUADRUPED = _PlanSpec(
    subject_noun="animal",
    head_noun="head",
    identity_traits="head, muzzle, eyes, fur/coat pattern, markings and body proportions",
    top=(
        "Top section (identity focus): one very large hero head close-up spanning ~50-60% width as the main visual anchor, "
        "beside a compact head rotation grid showing the SAME head at DISTINCT angles — never repeat the frontal view: "
        "front, three-quarter left, left profile, rear / back of head, looking up, looking down — plus one supporting head crop. "
        "This top row must immediately establish the animal's head identity: muzzle shape, eyes, ears and markings."
    ),
    middle=(
        "Middle section: three evenly spaced full-body panels — standing squarely on all four legs seen from the front, "
        "the same neutral four-legged stance seen from directly behind, and a three-quarter front view. "
        "All four limbs are legs planted on the ground."
    ),
    lower=(
        "Lower section: full left profile and full right profile — the profile silhouette is what defines this animal, "
        "so give both panels generous width — plus a three-quarter rear view and a natural walking gait. "
        "Do NOT include any top-down / overhead view (it distorts into blobs)."
    ),
    guard=(
        "ANATOMY (non-negotiable): this is a four-legged animal, NOT a humanoid and NOT anthropomorphic. "
        "No T-pose, no arms, no hands, no fingers, no human shoulders spread horizontally, no upright bipedal stance. "
        "The forelimbs are legs ending in paws/hooves and stay on the ground."
    ),
    detail_noun="coat and marking detail",
    sheet_noun="head sheet",
)

# Griffin / dragon: the quadruped layout, plus wings that must be shown both folded and
# at full span — a folded-only sheet gives the video model nothing to animate from.
_WINGED_QUADRUPED = _PlanSpec(
    subject_noun="creature",
    head_noun="head",
    identity_traits="head, fur/feather pattern, wing shape, markings and body proportions",
    top=(
        "Top section (identity focus): one very large hero head close-up spanning ~50-60% width as the main visual anchor, "
        "beside a compact head rotation grid showing the SAME head at DISTINCT angles — never repeat the frontal view: "
        "front, three-quarter left, left profile, rear / back of head, looking up, looking down — plus one supporting head crop. "
        "This top row must immediately establish the creature's head identity: muzzle or beak shape, eyes, horns or ears and markings."
    ),
    middle=(
        "Middle section: three evenly spaced full-body panels — standing squarely on all four legs seen from the front with the wings folded against the body, "
        "the same four-legged stance seen from directly behind with the wings folded, "
        "and a front view with the wings FULLY SPREAD to their full span."
    ),
    lower=(
        "Lower section: full left profile and full right profile with the wings folded — the profile silhouette is what defines this creature, "
        "so give both panels generous width — plus a three-quarter rear view with the wings spread and a natural walking gait. "
        "Do NOT include any top-down / overhead view (it distorts into blobs)."
    ),
    guard=(
        "ANATOMY (non-negotiable): this is a four-legged winged creature, NOT a humanoid and NOT anthropomorphic. "
        "No T-pose, no arms, no hands, no fingers, no human shoulders spread horizontally, no upright bipedal stance. "
        "The forelimbs are legs ending in paws/claws and stay on the ground. "
        "The wings are wings: they attach at the shoulders/back, they are never arms and never end in hands. "
        "Four legs plus two wings — six limbs total, no more."
    ),
    detail_noun="coat, feather and wing detail",
    sheet_noun="head sheet",
)

_AVIAN = _PlanSpec(
    subject_noun="bird",
    head_noun="head",
    identity_traits="head, beak, eyes, plumage pattern, markings and body proportions",
    top=(
        "Top section (identity focus): one very large hero head close-up spanning ~50-60% width as the main visual anchor, "
        "beside a compact head rotation grid showing the SAME head at DISTINCT angles — never repeat the frontal view: "
        "front, three-quarter left, left profile, rear / back of head, looking up, looking down — plus one supporting head crop. "
        "This top row must immediately establish the bird's head identity: beak shape, eyes, crest and plumage markings."
    ),
    middle=(
        "Middle section: three evenly spaced full-body panels — standing on two legs seen from the front with the wings folded, "
        "the same standing stance seen from directly behind, "
        "and a front view with the wings FULLY SPREAD to their full span."
    ),
    lower=(
        "Lower section: full left profile and full right profile with the wings folded, "
        "a three-quarter rear view with the wings spread, and one perched pose. "
        "Do NOT include any top-down / overhead view (it distorts into blobs)."
    ),
    guard=(
        "ANATOMY (non-negotiable): this is a bird, NOT a humanoid and NOT anthropomorphic. "
        "No T-pose, no arms, no hands, no fingers, no human shoulders. "
        "The forelimbs ARE the wings; the two legs end in taloned feet. "
        "Two legs plus two wings — four limbs total."
    ),
    detail_noun="plumage detail",
    sheet_noun="head sheet",
)

_PLANS: dict[str, _PlanSpec] = {
    "humanoid": _HUMANOID,
    "quadruped": _QUADRUPED,
    "wingedQuadruped": _WINGED_QUADRUPED,
    "avian": _AVIAN,
}


def build_character_sheet(
    style: Style,
    c: Character,
    bases: list[Character] | None = None,
    look: Look | None = None,
    *,
    has_identity_photos: bool = False,
    ref_manifest: str | None = None,
) -> str:
    """Build a 9:16 character turnaround reference-sheet prompt.

    *look* is the named outfit/state being rendered; its description is the ONLY clothing in
    the prompt, so another look's clothes cannot leak in. *bases* are the characters `c`
    @mentions in its description (a legacy identity variant) — their appearance is spelled out
    and the `@id` tokens are resolved to names. *has_identity_photos* is True when the
    character has real identity reference photos attached (Character.identity_refs)
    conditioning this sheet — the reference clause then reads as real photographs of the
    person rather than a generic "reference images" framing.

    *ref_manifest*, when non-empty, REPLACES the reference clause instead of joining it:
    the shipped clause tells the model to take clothing from no reference at all, which
    contradicts an outfit-role slot and would preserve the very blending the manifest
    exists to remove. Empty or None keeps today's output byte-for-byte.

    `c.body_plan` selects the panel layout. An unset or unrecognised value means humanoid,
    which reproduces this prompt exactly as it shipped before body plans existed.
    """
    bases = bases or []
    plan = _PLANS.get(norm_body_plan(c.body_plan), _HUMANOID)
    subject = clean_identity_description(
        strip_mentions(
            c.canonical_description, [{"id": b.id, "name": b.name} for b in bases]
        )
    )
    label = norm_label(look.label) if look else ""
    identity_only = (
        bool(bases) or has_identity_photos or (look is not None and label != "primary")
    )
    look_line = (
        f"Look (identical in all panels): {look.description.strip()}"
        if look and look.description.strip()
        else ""
    )
    medium_lead = (
        f"{style.global_preamble.strip()}." if style.global_preamble.strip() else ""
    )
    # With a manifest, the attached images ARE the description, and the written
    # description is dropped rather than reworded. This is not a preference: a live
    # render with a face, a body and a coat attached came back as the character's
    # TEXT — its hair, its eyes, its medieval half-armour — and none of the three
    # references. The prompt had said so twice. The subject line called the text
    # "keep identical everywhere", the look line ended "No modern clothing", and the
    # manifest sat ten lines below both, where the comment above explains it could
    # not win. Two sources for one trait is a coin toss; one source cannot contradict
    # itself. Per-image notes inside the manifest carry any nuance the text used to.
    #
    # Dropped whatever the kit covers, not only the overlapping part — a kit holding
    # just a prop still renders without the description, and the model invents what
    # nothing covers. That is the operator's explicit choice.
    if ref_manifest:
        subject_line = ""
        look_line = ""
    else:
        subject_line = f"Subject identity (keep identical everywhere): {subject}"
    return "\n".join(
        p
        for p in [
            # Medium first: the opening tokens dominate an image model's read, so the
            # project's chosen medium (photoreal / 3D / anime — from globalPreamble)
            # leads, before any layout scaffolding can bias the style. Reinforced again
            # in _style_block at the tail.
            medium_lead,
            f"9:16 character reference sheet showing the same {plan.subject_noun} from multiple distinct angles and poses.",
            # The manifest rides directly behind the medium for the same reason the
            # medium leads: what the references mean has to be read before the prose
            # it governs. Without a manifest this slot is empty and the reference
            # clause stays at its original place near the tail, byte for byte.
            ref_manifest or "",
            f"Same {plan.subject_noun} in every panel — identical {plan.identity_traits}. No redesign, no reinterpretation.",
            subject_line,
            look_line,
            _identity_anchor(bases),
            plan.top,
            plan.middle,
            plan.lower,
            plan.guard,
            (
                f"Full-body panels stay large enough to preserve proportions and {plan.detail_noun} while the {plan.sheet_noun} stays prioritised at the top; "
                "the composition must fully utilise the tall 9:16 frame."
            ),
            (
                f"Strong hierarchy: {plan.head_noun} identity first, body turnaround second. Every panel shows a genuinely different camera angle or pose — "
                "do NOT draw every panel facing forward; the rotation must actually rotate."
            ),
            ""
            if ref_manifest
            else _reference_clause(identity_only, has_identity_photos),
            _style_block(style),
            _common_tail(style.banned),
        ]
        if p
    )


def _identity_anchor(bases: list[Character]) -> str:
    """Describe the @mentioned base character(s) this one is a variant of.

    The sheet orders a large hero face close-up, so the face has to be specified in words
    too: conditioning on the base's sheet alone leaves the model free to invent the face it
    is enlarging, and it returns a lookalike. Mirrors the identity clause the scene/poster
    prompts already carry.
    """
    who = ". ".join(
        f"{b.name}: {desc}"
        for b in bases
        if (desc := clean_identity_description(b.canonical_description))
    )
    if not who:
        return ""
    return (
        f"IDENTITY ANCHOR — the reference images show this SAME person: {who.rstrip('. ')}. "
        "Reproduce that face EXACTLY: same bone structure, same eyes, nose and mouth, same skin "
        "tone and texture, same hair, same age. This is a WARDROBE/STYLING change only — not a new "
        "person, not a sibling, not a lookalike. Change only what the subject line changes. "
        "Take FACE and BODY from this anchor and nothing else: any clothing, outfit or accessories it "
        "mentions are the base's OLD wardrobe — ignore them entirely, the subject line above is the only "
        "wardrobe that exists."
    )


def _reference_clause(identity_only: bool, has_identity_photos: bool = False) -> str:
    """How to read the attached reference images.

    identity_only is True when the reference must supply IDENTITY ONLY — an identity
    variant's base, this character's own primary sheet while a new look is rendered, OR
    real identity photos the user uploaded. In every identity-only case the reference's
    clothing must not be copied, or half the panels come back in the wrong outfit.

    Three-way split:
      - not identity_only: the plain clause (reference may supply outfit too).
      - identity_only and not has_identity_photos: the ORIGINAL identity-only clause
        (identity-variant bases, any non-primary Look's own primary-sheet reference) —
        kept byte-for-byte so this shipped wording never silently drifts.
      - identity_only and has_identity_photos: the newer real-photo wording, which only
        applies when the reference is an actual uploaded photo of the person.
    """
    if not identity_only:
        return (
            "When reference images are provided, match their face, skin texture, hair, outfit and proportions EXACTLY "
            "— no redesign, no reinterpretation, photoreal identity preserved 100% across every panel."
        )
    if not has_identity_photos:
        return (
            "The reference images are there for IDENTITY ONLY: match their face, skin texture, hair and body "
            "proportions EXACTLY — no redesign, no reinterpretation, photoreal identity preserved 100% across every panel. "
            "Do NOT copy the clothing, outfit, accessories or styling from the reference images: the look described above "
            "REPLACES whatever the reference is wearing. Every single panel — including the face close-ups and the head "
            "rotation grid — shows the NEW look. No panel may show the reference's old clothes, and the two must never be "
            "mixed or blended."
        )
    return (
        "The reference images are real photographs of this person, provided for IDENTITY ONLY: "
        "match their face, skin texture, hair and body "
        "proportions EXACTLY — no redesign, no reinterpretation, identity preserved 100% across every panel. "
        "Do NOT copy the clothing, outfit, accessories, background or framing from the reference images: the look described above "
        "REPLACES whatever the reference is wearing. Every single panel — including the face close-ups and the head "
        "rotation grid — shows the described look, rendered in the project's style. No panel may show the reference's old clothes."
    )


def _common_tail(banned: str) -> str:
    # Backdrop is deliberately a neutral warm-grey, NOT white or black: character
    # sheets on grey generate more consistent identity than on white or black (borne out
    # by prompt testing, incl. the Higgsfield Seedance-4K breakdown). Don't "clean it up"
    # to white — the grey is load-bearing.
    #
    # The layout line names NO medium and NO CG-leaning format word. It used to say "like a
    # premium animation-studio turnaround board" — the only medium word in the whole prompt, so
    # a photoreal project still got a cartoon cast. Even after dropping "animation-studio",
    # "turnaround board" itself is a CG magnet: in training data, turnaround boards are
    # overwhelmingly 3D character-design sheets, and that format prior overrides photoreal
    # tokens. Medium comes from style.globalPreamble alone; keep this line about composition.
    return (
        "Layout: vertical 9:16 portrait canvas, laid out as a clean multi-panel reference sheet. "
        "Neutral warm-grey backdrop, soft even illumination, no harsh shadows, thin white gutters separating panels. "
        "Keep proportions, colors and details identical across every panel — no redesign, no reinterpretation. "
        f"no text, no labels, no watermarks.\nAvoid: {banned}"
    )


def _style_block(style: Style) -> str:
    return f"Style: {style.global_preamble}, applied consistently to every panel."


def build_location_view(
    style: Style, loc: Location, view_prompt: str | None = None
) -> str:
    """Build a SINGLE clean establishing frame for a location (not a multi-panel board)."""
    view = view_prompt.strip() if view_prompt else None
    subject = (
        f"{loc.canonical_description} This specific view: {view}."
        if view
        else loc.canonical_description
    )
    return "\n".join(
        [
            "A single photorealistic establishing photograph — ONE continuous frame, NOT a multi-panel board, grid, collage, split-screen or contact sheet.",
            f"{subject} Lighting: {loc.lighting_profile}.",
            "No people in frame.",
            (
                "If reference images are provided, this is the SAME place from a different camera angle — "
                "match their architecture, materials, colours and lighting EXACTLY; change only the viewpoint, no redesign."
            ),
            f"Style: {style.global_preamble}.",
            "Vertical 9:16, one unbroken frame — no panels, no dividing gutters, no multiple views, no labels, no text, no watermarks.",
            f"Avoid: {style.banned}",
        ]
    )


def build_prop_view(style: Style, p: Prop) -> str:
    """Build a SINGLE clean hero shot of a prop (not a multi-panel board).

    Mirrors build_location_view. A prop's identity is shape, colour and material —
    a six-panel grid starves exactly that detail, and image models echo the grid
    layout into keyframes conditioned on it. One object, one frame.
    """
    return "\n".join(
        [
            "A single product-style hero shot of ONE object — one continuous frame, "
            "NOT a multi-panel board, grid, collage, split-screen, contact sheet or inset.",
            f"Object: {p.canonical_description}",
            "The object is shown from a three-quarter angle, centered and filling most of the frame, "
            "on a neutral warm-grey backdrop with soft even illumination and no harsh shadows.",
            "Exactly one instance of the object — no repeated views, no alternate angles, no turnaround.",
            (
                "If reference images are provided, match their shape, proportions, colours and materials "
                "EXACTLY — no redesign, no reinterpretation."
            ),
            f"Style: {style.global_preamble}.",
            "One unbroken frame — no panels, no dividing gutters, no multiple views, no labels, no text, no watermarks.",
            f"Avoid: {style.banned}",
        ]
    )
