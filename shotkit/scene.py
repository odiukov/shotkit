"""scene — frame, poster and motion prompt assembly.

Port of app/application/storyboard.py (frame + poster builders) plus a new
build_motion_prompt whose body mirrors the tool's own assembly at
app/web/handlers/scene_request.py:676-695.
"""

from __future__ import annotations

from shotkit import poster
from shotkit.guards import (
    clean_identity_description,
    frame_safety_tail,
    reference_layout_clause,
    with_audio_discipline,
    with_i2v_safety,
    with_keyframe_anchor,
    with_spoken_line,
)
from shotkit.mentions import strip_mentions
from shotkit.types import Character, Location, Prop


# ---------------------------------------------------------------------------
# Prompt builders (pure)
# ---------------------------------------------------------------------------


def _identity_clause(
    chars: list[Character], look_desc_by_char: dict[str, str] | None = None
) -> str:
    """Who each character IS, plus what a TAGGED look says they are wearing.

    Frame/poster ONLY — this is `_identity_clause` from
    app/application/storyboard.py, emitted as `"Maintain identity: ..."`. The
    motion path has a DIFFERENT clause (`_who_is_who_clause`, below): different
    wording, a >=2-character threshold, and no wardrobe text at all — see its
    docstring for why the two must never be conflated.

    A `@id#label` used to condition the reference image and nothing else, so the prompt
    text could silently contradict it — and text wins. `strip_mentions` deletes the tag,
    so a scene reading "both fully clothed below the waist" sent the model that phrase
    with the word "shirtless" nowhere in it: the shirtless sheet was attached and the
    render put him in a t-shirt anyway (a clothing phrase reads as an instruction and
    overrides the sheet — see skills/cinematic-scenes/references/failure-modes.md).

    Only an EXPLICIT tag injects. A bare `@mention` adds no wardrobe prose: naming a
    garment for a ref-fixed character is the very failure this guards against, so the
    primary look's description must NOT leak into every keyframe.
    """
    look_desc_by_char = look_desc_by_char or {}
    parts: list[str] = []
    for c in chars:
        identity = c.canonical_description.strip()
        wearing = (look_desc_by_char.get(c.id) or "").strip()
        if not identity and not wearing:
            continue
        s = f"{c.name}: {identity}" if identity else f"{c.name}:"
        if wearing:
            s += f" Wearing: {wearing}"
        parts.append(s)
    return ". ".join(parts)


def _setting_clause(locations: list[Location]) -> str:
    parts = []
    for loc in locations:
        if not loc.canonical_description.strip():
            continue
        s = f"{loc.name}: {loc.canonical_description.strip()}"
        if loc.lighting_profile and loc.lighting_profile.strip():
            s += f" Lighting: {loc.lighting_profile.strip()}."
        parts.append(s)
    return " ".join(parts)


def _props_clause(props: list[Prop]) -> str:
    return ". ".join(
        f"{p.name}: {p.canonical_description.strip()}"
        for p in props
        if p.canonical_description.strip()
    )


def build_scene_frame_prompt(
    scene_prompt: str,
    chars: list[Character],
    locations: list[Location],
    props: list[Prop],
    preamble: str,
    banned: str = "",
    look_desc_by_char: dict[str, str] | None = None,
) -> str:
    """Build a single cinematic keyframe prompt."""
    identity = _identity_clause(chars, look_desc_by_char)
    setting = _setting_clause(locations)
    prop_list = _props_clause(props)
    parts = [
        preamble,
        reference_layout_clause(len(chars)) if (chars or props) else "",
        f"Single cinematic keyframe. {scene_prompt.strip()}.",
        "A single photograph from one camera angle, one continuous image that fills the whole frame edge to edge.",
        "A single frozen instant — the state at this exact moment, no motion blur, no before-and-after, no transition.",
        f"Setting: {setting}" if setting else "",
        f"Props: {prop_list}" if prop_list else "",
        f"Maintain identity: {identity}." if identity else "",
        frame_safety_tail(banned),
    ]
    return "\n".join(p for p in parts if p)


def build_poster_prompt(
    scene_prompt: str,
    chars: list[Character],
    locations: list[Location],
    props: list[Prop],
    preamble: str,
    banned: str = "",
    look_desc_by_char: dict[str, str] | None = None,
    focus_y: float | None = None,
) -> str:
    """Build a vertical theatrical movie-poster (key-art) prompt.

    `focus_y` is the crop offset a story-card player will apply, so the composition
    clause names the band that actually reaches the card — but shotkit has no
    particular card of its own (see shotkit/poster.py's module docstring). The
    clause is emitted ONLY when the scene actually asks for a crop band: `focus_y`
    not None (i.e. a `posterFocusY` field present in the scene data). A project
    with no story card must not be told most of its poster is cropped away for a
    card it doesn't have.
    """
    identity = _identity_clause(chars, look_desc_by_char)
    setting = _setting_clause(locations)
    prop_list = _props_clause(props)
    parts = [
        preamble,
        reference_layout_clause(len(chars)) if (chars or props) else "",
        f"Theatrical movie poster key art, vertical 9:16 portrait composition. {scene_prompt.strip()}.",
        "A single polished poster image with a clear focal hierarchy and dramatic cinematic lighting.",
        poster.compose_clause(focus_y) if focus_y is not None else "",
        f"Setting: {setting}" if setting else "",
        f"Props: {prop_list}" if prop_list else "",
        f"Maintain identity: {identity}." if identity else "",
        frame_safety_tail(banned),
    ]
    return "\n".join(p for p in parts if p)


# ---------------------------------------------------------------------------
# Motion prompt assembly
# ---------------------------------------------------------------------------


def _who_is_who_clause(chars: list[Character]) -> str:
    """The MOTION path's who-is-who clause — scene_request.py:602-617, verbatim.

    NOT the frame/poster `_identity_clause` above, and not interchangeable with it:

    - **Threshold:** only at TWO OR MORE mentioned characters with a non-empty
      description. On the default (no-keyframe) path the model receives N
      unlabeled reference images plus this prompt text; with 2+ characters it has
      no inherent binding of which image is which name and swaps them. With ONE
      character there is nothing to swap, so the tool emits nothing.
    - **Wording:** `"Character identities — match each face to its reference
      image: <Name>: <desc> …"`, trailing space, prepended directly (no "Maintain
      identity" — that string belongs only to the frame/poster clause above).
    - **Cleaning:** each description passes through `clean_identity_description`
      first. Not cosmetic: `canonical_description` is authored prose that can end
      with a directive aimed at whoever fills the field ("Identity only — no
      clothing here."). Pasted into a clip prompt verbatim, those words are just
      content next to a described body — a provider's pre-generation moderator
      reads "no clothing" as a request for the opposite of what it says and
      refuses the whole job as sensitive.
    - **No wardrobe text.** Unlike the frame/poster clause, this one never adds a
      tagged look's "Wearing: ..." — the tool's motion assembly has no such thing.
    """
    mentioned = [
        (c, clean_identity_description(c.canonical_description))
        for c in chars
        if c.canonical_description.strip()
    ]
    mentioned = [(c, desc) for c, desc in mentioned if desc]
    if len(mentioned) < 2:
        return ""
    who = " ".join(f"{c.name}: {desc}" for c, desc in mentioned)
    return f"Character identities — match each face to its reference image: {who} "


def _loop_hint(motion_prompt: str, loop: bool) -> str:
    """Append the seamless-loop clause when *loop* is set (mirrors the tool's own
    `_loop_hint`, app/web/handlers/scene_request.py:360).

    A fork clip pins the keyframe as both first and last frame, but that anchor alone only
    constrains the ENDPOINTS — the model still fills the middle with a push-in then yanks back to
    the end frame (a "breathing zoom" that snaps at the tail). So the loop clause must ALSO lock the
    camera and keep motion minimal so the in-between never drifts and the loop closes with no snap.
    """
    if not loop:
        return motion_prompt
    loop_clause = (
        "Seamless loop: the clip must begin and end on the exact same frame. "
        "Locked-off static camera — no zoom, no push-in, no pull-back, no dolly, no pan, no tilt; "
        "focal length, framing and subject scale identical for the entire clip. "
        "Keep all motion minimal and continuous so the final frame returns to the first with no snap or jump."
    )
    m = motion_prompt.strip()
    return f"{m}. {loop_clause}" if m else loop_clause


MOTION_MODES = ("i2v", "t2v", "ref-anchored")


def build_motion_prompt(
    motion_prompt: str,
    *,
    mode: str,
    chars: list[Character],
    dialogue: str = "",
    generate_audio: bool = True,
    loop: bool = False,
    refs_for_strip: list[dict] | None = None,
    voices: dict | None = None,
) -> str:
    """Assemble what a video model receives, in the tool's exact order.

    who-is-who -> authored motion -> loop hint -> spoken line and narration ->
    exactly ONE mode clause -> audio discipline -> mentions stripped.

    The three modes are not interchangeable:
      "i2v"          a seed frame exists; the model must animate only what it shows.
      "ref-anchored" the keyframe travels as reference #1 among peers, so the prompt
                     has to say that reference #1 IS frame 0 — otherwise the model
                     reads it as one more mood-board image and re-composes the shot.
      "t2v"          no frame at all; the model composes from prompt and references,
                     and BOTH of the above clauses would be lies.

    `voices` is the speaker -> {gender, voiceNote} map `guards.narrator_voice_map`
    builds (see `project.py::render_motion`, which builds it from the WHOLE
    project roster, not just `chars` — a `VO:` speaker need not be @mentioned in
    this scene's motionPrompt to have a pinned voice, exactly as in the tool).
    """
    if mode not in MOTION_MODES:
        raise ValueError(
            f"unknown motion mode {mode!r}; expected one of {MOTION_MODES}"
        )

    identity = _who_is_who_clause(chars)
    out = identity + (motion_prompt or "")
    out = _loop_hint(out, loop)
    # Dialogue is gated on the same flag as the audio tail, exactly as the tool gates it.
    # Telling a model to speak a line "aloud, naturally and in sync" in a clip that bakes
    # no audio track is a contradiction the model resolves by moving lips to nothing.
    out = with_spoken_line(out, (dialogue or "") if generate_audio else "", voices)
    if mode == "ref-anchored":
        out = with_keyframe_anchor(out)
    elif mode == "i2v":
        out = with_i2v_safety(out)
    out = with_audio_discipline(out, generate_audio)
    return strip_mentions(out, refs_for_strip or [])
